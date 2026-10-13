<template>
  <div class="link-validator">
    <header class="header">
      <div class="header__logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.72"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.72-1.72"></path></svg>
      </div>
      <h1 class="header__title">Link Checker</h1>
    </header>
    <main class="main-grid">
      <div class="card">
        <h3>1. Select Sources</h3>
        <div class="source-buttons">
          <button @click="openFilePicker('directory')">Directory</button>
          <button @click="openFilePicker('files')">Files</button>
        </div>
        <div v-if="files.length > 0" class="selection-info">
          <p>{{ files.length }} file(s) selected.</p>
          <button @click="clearSelection" class="selection-info__clear-btn">Clear</button>
        </div>
        <p v-else class="scan-info">Scans .html and .json files</p>
        <input type="file" ref="fileInput" @change="handleFileChange" multiple style="display: none" />
        <input type="file" ref="directoryInput" @change="handleFileChange" webkitdirectory directory style="display: none" />

        <div v-if="showReferenceSelector" class="reference-section">
          <hr />
          <h3>2. Select Reference Directory</h3>
          <div class="source-buttons">
            <button @click="openFilePicker('reference')">Reference Directory</button>
          </div>
          <div v-if="referenceFiles.length > 0" class="selection-info">
            <p>{{ referenceFiles.length }} reference file(s) selected.</p>
          </div>
          <p v-else class="scan-info">Select a directory of files for context.</p>
          <input type="file" ref="referenceDirectoryInput" @change="handleReferenceFileChange" webkitdirectory directory style="display: none" />
        </div>
      </div>
      <div class="card">
        <h3>Scan Statistics</h3>
        <div class="stats-grid">
          <div>
            <div class="stat__value">{{ totalLinks }}</div>
            <div class="stat__label">TOTAL LINKS</div>
          </div>
          <div>
            <div class="stat__value stat__value--checked">{{ checkedLinks }}</div>
            <div class="stat__label">CHECKED</div>
          </div>
          <div>
            <div class="stat__value stat__value--broken">{{ brokenLinks }}</div>
            <div class="stat__label">BROKEN</div>
          </div>
          <div>
            <div class="stat__value stat__value--redirects">{{ redirectLinks }}</div>
            <div class="stat__label">REDIRECTS</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="scan-control">
          <label for="site-name"><strong>Site Name</strong></label>
          <input type="text" id="site-name" v-model="siteName" placeholder="Optional, for CSV filename" />
          <button @click="checkLinks" :disabled="files.length === 0 || isLoading">
            {{ isLoading ? 'Scanning...' : 'Start Link Check' }}
          </button>
        </div>
        <div class="progress-bar">
          <div class="progress-bar__fill" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="progress-bar__text">
          <span>{{ isLoading ? 'Ready' : 'Ready' }}</span>
          <span>{{ progress.toFixed(0) }}%</span>
        </div>
      </div>
    </main>

    <!-- Toggle Button for Column Visibility Controls -->
    <div class="column-controls">
      <button
        @click="showColumnControls = !showColumnControls"
        class="column-controls__toggle"
      >
        {{ showColumnControls ? 'Hide Column Controls' : 'Show Column Controls' }}
      </button>
    </div>

    <!-- Column Visibility Controls -->
    <div v-if="showColumnControls" class="column-visibility">
      <div class="column-visibility__labels">
        <label v-for="col in columnOptions" :key="col.key" class="column-visibility__label">
          <input type="checkbox" v-model="visibleColumns[col.key]" />
          {{ col.label }}
        </label>
      </div>
    </div>

    <div class="card card--results">
      <div class="tabs">
        <div class="tabs__controls">
          <button @click="activeTab = 'Broken'" :class="{ active: activeTab === 'Broken' }">Broken <span>{{ brokenLinks }}</span></button>
          <button @click="activeTab = 'Redirecting'" :class="{ active: activeTab === 'Redirecting' }">Redirects <span>{{ redirectLinks }}</span></button>
          <button @click="activeTab = 'All'" :class="{ active: activeTab === 'All' }">All <span>{{ totalLinks }}</span></button>
        </div>
        <button @click="downloadCSV(activeTab)" :disabled="!scanCompleted" class="tabs__csv-btn">
          CSV
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-down"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 12 19 5 12"></polyline></svg>
        </button>
      </div>
      <div class="results-table">
        <table>
          <thead>
            <tr>
              <th v-if="visibleColumns.status" @click="sortBy('status')" class="sortable">
                <span class="table-header">
                  Status
                  <span class="table-header__arrows">
                    <span :class="{ active: sortKey === 'status' && sortOrder === 'asc' }">▲</span>
                    <span :class="{ active: sortKey === 'status' && sortOrder === 'desc' }">▼</span>
                  </span>
                </span>
              </th>
              <th v-if="visibleColumns.link" @click="sortBy('link')" class="sortable">
                <span class="table-header">
                  URL
                  <span class="table-header__arrows">
                    <span :class="{ active: sortKey === 'link' && sortOrder === 'asc' }">▲</span>
                    <span :class="{ active: sortKey === 'link' && sortOrder === 'desc' }">▼</span>
                  </span>
                </span>
              </th>
              <th v-if="visibleColumns.sourceFile" @click="sortBy('sourceFile')" class="sortable">
                <span class="table-header">
                  Source File
                  <span class="table-header__arrows">
                    <span :class="{ active: sortKey === 'sourceFile' && sortOrder === 'asc' }">▲</span>
                    <span :class="{ active: sortKey === 'sourceFile' && sortOrder === 'desc' }">▼</span>
                  </span>
                </span>
              </th>
              <th v-if="visibleColumns.linkText" @click="sortBy('linkText')" class="sortable">
                <span class="table-header">
                  Link Text
                  <span class="table-header__arrows">
                    <span :class="{ active: sortKey === 'linkText' && sortOrder === 'asc' }">▲</span>
                    <span :class="{ active: sortKey === 'linkText' && sortOrder === 'desc' }">▼</span>
                  </span>
                </span>
              </th>
              <th v-if="visibleColumns.details" @click="sortBy('details')" class="sortable">
                <span class="table-header">
                  Details / Location
                  <span class="table-header__arrows">
                    <span :class="{ active: sortKey === 'details' && sortOrder === 'asc' }">▲</span>
                    <span :class="{ active: sortKey === 'details' && sortOrder === 'desc' }">▼</span>
                  </span>
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredResults.length === 0">
              <td :colspan="Object.values(visibleColumns).filter(Boolean).length" class="no-links">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5l-1.5 1.5l-5-5v-.79l-.27-.27A6.516 6.516 0 0 1 9.5 16A6.5 6.5 0 0 1 3 9.5A6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14S14 12 14 9.5S12 5 9.5 5Z"/></svg>
                <p>No links found for this category.</p>
              </td>
            </tr>
            <tr v-for="result in filteredResults" :key="`${result.link}-${result.sourceFile}`">
              <td v-if="visibleColumns.status"><span :class="['status-badge', `status-badge--${(result.status || '').toLowerCase()}`]">{{ result.status || '' }}</span></td>
              <td v-if="visibleColumns.link" class="url-cell"><a :href="result.link || '#'" target="_blank" rel="noopener noreferrer">{{ result.link || '' }}</a></td>
              <td v-if="visibleColumns.sourceFile" class="source-file-cell">{{ result.sourceFile || '' }}</td>
              <td v-if="visibleColumns.linkText" class="link-text-cell">{{ result.linkText || '' }}</td>
              <td v-if="visibleColumns.details" class="details-cell">
                <a v-if="result.status === 'Redirecting' || result.status === 'Redirecting secure'" :href="result.details || '#'" target="_blank" rel="noopener noreferrer">
                  {{ result.details || '' }}
                </a>
                <span v-else>{{ result.details || '' }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useLinkChecker } from '../js/LinkChecker.js';
import '../scss/site.scss';
 
const {
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
  fileInput,
  directoryInput,
  referenceDirectoryInput,
  totalLinks,
  checkedLinks,
  brokenLinks,
  redirectLinks,
  filteredResults,
  sortBy,
  openFilePicker,
  clearSelection,
  handleFileChange,
  handleReferenceFileChange,
  checkLinks,
  downloadCSV
} = useLinkChecker();
</script>