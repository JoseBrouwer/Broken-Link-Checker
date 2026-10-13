import { ref, computed, reactive } from 'vue';

/**
 * @template T
 * @typedef {Object} Ref
 * @property {T} value - The reactive value
 */

/**
 * @template T
 * @typedef {Object} ComputedRef
 * @property {T} value - The computed reactive value (read-only)
 */

/**
 * @typedef {Object} LinkResult
 * @property {string} link - The URL of the link
 * @property {string} sourceFile - The file(s) where the link was found
 * @property {string} linkText - The anchor text or label for the link
 * @property {string} status - The status of the link ('Pending', 'OK', 'Broken', 'Redirecting', 'Redirecting secure')
 * @property {string} details - Additional information about the link (error message or redirect URL)
 */

/**
 * @typedef {Object} ColumnOption
 * @property {string} key - The unique identifier for the column
 * @property {string} label - The display label for the column
 */

/**
 * Composable function for link checking functionality in Vue 3.
 * Provides state management and methods for scanning files, checking links,
 * and managing results display.
 */
export function useLinkChecker() {
    /** @type {Ref<File[]>} Array of selected files to scan */
    const files = ref([]);

    /** @type {Ref<File[]>} Array of reference HTML files for context matching */
    const referenceFiles = ref([]);
    
    /** @type {Ref<LinkResult[]>} Array of link check results */
    const results = ref([]);
    
    /** @type {Ref<boolean>} Loading state during link checking */
    const isLoading = ref(false);
    
    /** @type {Ref<number>} Progress percentage (0-100) */
    const progress = ref(0);
    
    /** @type {Ref<string>} Active results tab ('All', 'Broken', 'Redirecting') */
    const activeTab = ref('All');
    
    /** @type {Ref<boolean>} Whether scan has been completed */
    const scanCompleted = ref(false);
    
    /** @type {Ref<boolean>} Whether to show reference directory selector */
    const showReferenceSelector = ref(false);
    
    /** @type {Ref<string>} Current sort column key */
    const sortKey = ref('');
    
    /** @type {Ref<string>} Current sort order ('asc' or 'desc') */
    const sortOrder = ref('asc');
    
    /** @type {Ref<string>} Optional site name for CSV filename */
    const siteName = ref('');
    
    /** @type {Ref<boolean>} Whether to show column visibility controls */
    const showColumnControls = ref(false);

    /**
     * Available column options for the results table
     * @type {ColumnOption[]}
     */
    const columnOptions = [
        { key: 'status', label: 'Status' },
        { key: 'link', label: 'URL' },
        { key: 'sourceFile', label: 'Source File' },
        { key: 'linkText', label: 'Link Text' },
        { key: 'details', label: 'Details / Location' }
    ];
    
    /**
     * Reactive object tracking which columns are visible
     * @type {Object.<string, boolean>}
     */
    const visibleColumns = reactive({
        status: true,
        link: true,
        sourceFile: true,
        linkText: true,
        details: true
    });

    /**
     * Computed property to determine if link text column should be shown.
     * Only displays if at least one result has non-empty link text.
     * @type {ComputedRef<boolean>}
     */
    const showLinkTextColumn = computed(() => {
    return results.value.some(result => result.linkText && result.linkText.trim() !== '');
    });

    /** @type {Ref<HTMLInputElement|null>} Reference to file input element */
    const fileInput = ref(null);
    
    /** @type {Ref<HTMLInputElement|null>} Reference to directory input element */
    const directoryInput = ref(null);
    
    /** @type {Ref<HTMLInputElement|null>} Reference to reference directory input element */
    const referenceDirectoryInput = ref(null);

    /**
     * Total number of links found in scanned files
     * @type {ComputedRef<number>}
     */
    const totalLinks = computed(() => results.value.length);
    
    /**
     * Number of links that have been checked (non-pending status)
     * @type {ComputedRef<number>}
     */
    const checkedLinks = computed(() => results.value.filter(r => r.status !== 'Pending').length);
    
    /**
     * Number of broken links found
     * @type {ComputedRef<number>}
     */
    const brokenLinks = computed(() => results.value.filter(r => r.status === 'Broken').length);
    
    /**
     * Number of redirecting links found (including secure redirects)
     * @type {ComputedRef<number>}
     */
    const redirectLinks = computed(() => results.value.filter(r => r.status === 'Redirecting' || r.status === 'Redirecting secure').length);

    /**
     * Filtered and sorted results based on active tab and sort settings.
     * Filters by tab category (All/Broken/Redirecting) and applies sorting if set.
     * @type {ComputedRef<LinkResult[]>}
     */
    const filteredResults = computed(() => {
    let data = results.value;

    if (activeTab.value === 'Redirecting') {
        data = results.value.filter(r => r.status === 'Redirecting' || r.status === 'Redirecting secure');
    } else if (activeTab.value !== 'All') {
        data = results.value.filter(r => r.status === activeTab.value);
    }

    if (sortKey.value) {
        data = data.slice().sort((a, b) => {
        const aValue = a[sortKey.value];
        const bValue = b[sortKey.value];
        if (aValue < bValue) return sortOrder.value === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortOrder.value === 'asc' ? 1 : -1;
        return 0;
        });
    }

    return data;
    });

    /**
     * Updates the sort key and order for results table.
     * Toggles between ascending and descending when clicking the same column.
     * @function sortBy
     * @param {string} key - The column key to sort by
     * @returns {void}
     */
    const sortBy = (key) => {
        if (sortKey.value === key) {
            sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
        } else {
            sortKey.value = key;
            sortOrder.value = 'asc';
        }
    };

    /**
     * Triggers the appropriate file picker based on type.
     * @function openFilePicker
     * @param {'files'|'directory'|'reference'} type - The type of picker to open
     * @returns {void}
     */
    const openFilePicker = (type) => {
        if (type === 'files') {
            fileInput.value.click();
        } else if (type === 'directory') {
            directoryInput.value.click();
        } else if (type === 'reference') {
            referenceDirectoryInput.value.click();
        }
    };

    /**
     * Clears all selected files, results, and resets the scanner state.
     * Resets file inputs and all associated state to initial values.
     * @function clearSelection
     * @returns {void}
     */
    const clearSelection = () => {
        files.value = [];
        results.value = [];
        progress.value = 0;
        scanCompleted.value = false;
        showReferenceSelector.value = false;
        referenceFiles.value = [];

        if (fileInput.value) 
            fileInput.value.value = null;
        if (directoryInput.value) 
            directoryInput.value.value = null;
        if (referenceDirectoryInput.value) 
            referenceDirectoryInput.value.value = null;
    };

    /**
     * Handles file selection from file/directory picker.
     * Filters for .html and .json files, extracts links from them,
     * and populates the results array with pending link checks.
     * Shows reference selector if a single JSON file is selected.
     * @function handleFileChange
     * @async
     * @param {Event} event - The file input change event
     * @returns {Promise<void>}
     */
    const handleFileChange = async (event) => {
        const selectedFiles = Array.from(event.target.files);

        // Clear previous selections
        files.value = [];
        results.value = [];

        const newFiles = selectedFiles.filter(file => {
            const path = file.webkitRelativePath || file.name;
            const supported = path.endsWith('.html') || path.endsWith('.json');
            if (!supported) {
            return false;
            }
            return supported;
        });

        if (newFiles.length === 0) {
            return;
        }

        files.value = newFiles;

        progress.value = 0;
        scanCompleted.value = false;

        const isDirectory = files.value.length > 0 && files.value.some(f => f.webkitRelativePath);
        const isSingleFile = files.value.length === 1 && !isDirectory;
        showReferenceSelector.value = isSingleFile && (files.value[0].webkitRelativePath || files.value[0].name).endsWith('.json');

        // Map to track unique links and their sources
        // Key: URL string, Value: { sources: Set<string>, linkTexts: Set<string> }
        const linkSources = new Map();

        // Process each file and extract links
        for (const file of files.value) {
            try {
            const content = await file.text();
            const filePath = file.webkitRelativePath || file.name;
            
            // Extract links from HTML files
            if (filePath.endsWith('.html')) {
                const parser = new DOMParser();
                const doc = parser.parseFromString(content, 'text/html');
                const anchors = doc.getElementsByTagName('a');
                let foundCount = 0;
                for (let i = 0; i < anchors.length; i++) {
                const href = anchors[i].getAttribute('href');
                const linkText = anchors[i].textContent.trim();
                if (href && (href.startsWith('http://') || href.startsWith('https://'))) {
                    if (!linkSources.has(href)) {
                    linkSources.set(href, { sources: new Set(), linkTexts: new Set() });
                    }
                    linkSources.get(href).sources.add(filePath);
                    if (linkText) {
                    linkSources.get(href).linkTexts.add(linkText);
                    }
                    foundCount++;
                }
                }
            } else if (filePath.endsWith('.json')) {
                // Extract links from JSON files
                try {
                const jsonData = JSON.parse(content);
                // Check if JSON has structured links array
                if (Array.isArray(jsonData.links)) {
                    for (const link of jsonData.links) {
                    if (link.url && (link.url.startsWith('http://') || link.url.startsWith('https://'))) {
                        if (!linkSources.has(link.url)) {
                        linkSources.set(link.url, { sources: new Set(), linkTexts: new Set() });
                        }
                        linkSources.get(link.url).sources.add(filePath);
                    }
                    }
                } else {
                    // Fallback: use regex to extract any URLs from JSON content
                    const jsonRegex = /https?:\/\/[^\s/$.?#].[^\s"]*/gi;
                    const foundLinks = content.match(jsonRegex) || [];
                    for (const link of foundLinks) {
                        if (link.startsWith('http://') || link.startsWith('https://')) {
                        if (!linkSources.has(link)) {
                            linkSources.set(link, { sources: new Set(), linkTexts: new Set() });
                        }
                        linkSources.get(link).sources.add(filePath);
                        }
                    }
                }
                } catch(e) {
                    // If JSON parsing fails, fall back to regex extraction
                    const jsonRegex = /https?:\/\/[^\s/$.?#].[^\s"]*/gi;
                    const foundLinks = content.match(jsonRegex) || [];
                    for (const link of foundLinks) {
                    if (link.startsWith('http://') || link.startsWith('https://')) {
                        if (!linkSources.has(link)) {
                        linkSources.set(link, { sources: new Set(), linkTexts: new Set() });
                        }
                        linkSources.get(link).sources.add(filePath);
                    }
                    }
                }
            }
            } catch (error) {
            console.error(`Error processing file: ${file.name}`, error);
            }
        }

        // Convert Map to results array with pending status
        results.value = Array.from(linkSources.entries()).map(([link, data]) => ({
            link,
            sourceFile: Array.from(data.sources).join(', '),
            linkText: Array.from(data.linkTexts).join(' | '),
            status: 'Pending',
            details: ''
        }));
    };

    /**
     * Handles reference directory selection for JSON file context matching.
     * Matches link IDs from JSON file with data-linkapi-id attributes in HTML files
     * to determine which links are actually used and their context.
     * Updates results with source file names and link text from reference files.
     * @function handleReferenceFileChange
     * @async
     * @param {Event} event - The file input change event
     * @returns {Promise<void>}
     */
    const handleReferenceFileChange = async (event) => {
        referenceFiles.value = Array.from(event.target.files).filter(file => file.name.endsWith('.html'));

        if (showReferenceSelector.value && referenceFiles.value.length > 0) {
            const jsonFile = files.value.find(f => f.name.endsWith('.json'));
            if (jsonFile) {
            // Build map of link IDs to URLs from JSON file
            const linkIdMap = new Map();
            const jsonContent = await jsonFile.text();
            try {
                const jsonData = JSON.parse(jsonContent);
                if (Array.isArray(jsonData.links)) {
                for (const link of jsonData.links) {
                    const idKey = Object.keys(link).find(key => key.toLowerCase().includes('id'));
                    if (idKey && link[idKey] && link.url) {
                    linkIdMap.set(link[idKey].toString(), link.url);
                    }
                }
                }
            } catch (e) {
                console.error("Error parsing JSON file for link IDs:", e);
            }

            // Scan reference HTML files for elements with data-linkapi-id attributes
            const urlToInfoMap = new Map();
            for (const file of referenceFiles.value) {
                const content = await file.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(content, 'text/html');
                const elementsWithId = doc.querySelectorAll('[data-linkapi-id]');
                for (let i = 0; i < elementsWithId.length; i++) {
                const element = elementsWithId[i];
                const linkId = element.getAttribute('data-linkapi-id');
                if (linkId && linkIdMap.has(linkId)) {
                    const url = linkIdMap.get(linkId);
                    if (!urlToInfoMap.has(url)) {
                    urlToInfoMap.set(url, []);
                    }
                    urlToInfoMap.get(url).push({ file: file.name, text: element.textContent.trim() });
                }
                }
            }

            // Update results with information from reference files
            let updated = false;
            if (urlToInfoMap.size > 0) {
                updated = true;
                for (const [url, infos] of urlToInfoMap.entries()) {
                const resultIndex = results.value.findIndex(r => r.link === url);
                if (resultIndex !== -1) {
                    results.value[resultIndex].sourceFile = infos.map(i => i.file).join(', ');
                    results.value[resultIndex].linkText = infos.map(i => i.text).join(' | ');
                    results.value[resultIndex].details = '';
                }
                }
            }

            // Mark URLs that exist in JSON but are not used in any reference file
            const jsonUrls = new Set(linkIdMap.values());
            const foundUrls = new Set(urlToInfoMap.keys());
            const notFoundUrls = new Set([...jsonUrls].filter(url => !foundUrls.has(url)));

            if (notFoundUrls.size > 0) {
                updated = true;
                for (const url of notFoundUrls) {
                const resultIndex = results.value.findIndex(r => r.link === url);
                if (resultIndex !== -1) {
                    results.value[resultIndex].sourceFile = 'Not Used!';
                    results.value[resultIndex].details = '';
                }
                }
            }

            if (updated) {
                // Force reactivity update
                results.value = [...results.value];
            }
            }
        }
    };



    /**
     * Checks all pending links by sending requests to the server API.
     * Updates each link's status (OK/Broken/Redirecting) and details.
     * Distinguishes between regular redirects and secure (http→https) redirects.
     * Updates progress as links are checked.
     * @function checkLinks
     * @async
     * @returns {Promise<void>}
     */
    const checkLinks = async () => {
        if (files.value.length === 0) return;

        isLoading.value = true;
        scanCompleted.value = false;
        progress.value = 0;

        const linksToCheck = results.value.map(r => r.link);
        let checkedCount = 0;

        for (let i = 0; i < linksToCheck.length; i++) {
            try {
            // Add timestamp to prevent caching
            const timestamp = new Date().getTime();
            const response = await fetch(`/api/check-link?url=${encodeURIComponent(linksToCheck[i])}&t=${timestamp}`);
            const data = await response.json();
            const resultIndex = results.value.findIndex(r => r.link === linksToCheck[i]);
            if (resultIndex !== -1) {
                const originalLink = linksToCheck[i];
                const newLink = data.details;
                let status = data.status;

                // Check if it's a secure redirect (http→https only)
                if (status === 'Redirecting' && newLink) {
                const secureRedirect = originalLink.startsWith('http://') &&
                                        newLink.startsWith('https://') &&
                                        originalLink.substring(7) === newLink.substring(8);
                if (secureRedirect) {
                    status = 'Redirecting secure';
                }
                }
                results.value[resultIndex].status = status;
                results.value[resultIndex].details = data.details;
            }
            } catch (error) {
            const resultIndex = results.value.findIndex(r => r.link === linksToCheck[i]);
            if (resultIndex !== -1) {
                results.value[resultIndex].status = 'Broken';
                results.value[resultIndex].details = 'Failed to check link';
            }
            }
            checkedCount++;
            progress.value = (checkedCount / totalLinks.value) * 100;
        }

        isLoading.value = false;
        scanCompleted.value = true;
    };

    /**
     * Generates and downloads a CSV file of link check results.
     * Filters data by category and includes relevant columns based on visibility.
     * Filename includes optional site name and current date.
     * @function downloadCSV
     * @param {'All'|'Broken'|'Redirecting'} category - The category of links to export
     * @returns {void}
     */
    const downloadCSV = (category) => {
        let dataToExport = [];
        let baseFilename = 'links';

        // Filter data based on selected category
        switch (category) {
            case 'Broken':
            dataToExport = results.value.filter(r => r.status === 'Broken');
            baseFilename = 'broken_links';
            break;
            case 'Redirecting':
            dataToExport = results.value.filter(r => r.status === 'Redirecting' || r.status === 'Redirecting secure');
            baseFilename = 'redirecting_links';
            break;
            case 'All':
            dataToExport = results.value;
            baseFilename = 'all_links';
            break;
        }

        if (dataToExport.length === 0) {
            return;
        }

        // Generate filename with date stamp
        const date = new Date();
        const dateStamp = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        const filename = siteName.value
            ? `${siteName.value.replace(/\s+/g, '-')}-${baseFilename}-${dateStamp}.csv`
            : `${baseFilename}-${dateStamp}.csv`;

        // Build CSV headers
        const headers = ['Status', 'URL', 'Source File'];
        if (showLinkTextColumn.value) {
            headers.push('Link Text');
        }
        headers.push('Details / Location');

        // Build CSV content with proper escaping
        const csvContent = [
            headers,
            ...dataToExport.map(item => {
            const row = [
                item.status,
                `"${item.link}"`,
                `"${item.sourceFile}"`,
            ];
            if (showLinkTextColumn.value) {
                row.push(`"${item.linkText}"`);
            }
            row.push(`"${item.details.replace(/"/g, '""').replace('Redirects to: ', '')}"`);
            return row;
            })
        ].map(e => e.join(',')).join('\n');

        // Create and trigger download with BOM for Excel compatibility
        const blob = new Blob([`\uFEFF${csvContent}`], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        if (link.href) {
            URL.revokeObjectURL(link.href);
        }
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    /**
     * Return all reactive state and methods for use in components
     */
    return {
        // Reactive state
        files,
        referenceFiles,
        results,
        isLoading,
        progress,
        activeTab,
        scanCompleted,
        showReferenceSelector,
        sortKey,
        sortOrder,
        siteName,
        showColumnControls,
        columnOptions,
        visibleColumns,
        showLinkTextColumn,
        
        // Template refs
        fileInput,
        directoryInput,
        referenceDirectoryInput,
        
        // Computed properties
        totalLinks,
        checkedLinks,
        brokenLinks,
        redirectLinks,
        filteredResults,
        
        // Methods
        sortBy,
        openFilePicker,
        clearSelection,
        handleFileChange,
        handleReferenceFileChange,
        checkLinks,
        downloadCSV
    };
}