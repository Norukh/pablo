const applyStyleSection = document.getElementById('apply-style-section');
const reportSection = document.getElementById('report-section');

export function hideAllSections() {
    applyStyleSection.classList.add('hidden');
    reportSection.classList.add('hidden');
}

export function showApplyStyleSection() {
    hideAllSections();
    applyStyleSection.classList.remove('hidden');
}

export function showReportSection() {
    hideAllSections();
    reportSection.classList.remove('hidden');
}