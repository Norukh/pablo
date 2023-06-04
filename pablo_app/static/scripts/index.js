import {applyStyle, getArtists, getPaintings} from "./services/artist-service.js";
import {isEmpty} from "./utils/utils.js";
import {BASE_URL} from "./utils/constants.js";
import {hideAllSections, showApplyStyleSection, showReportSection} from "./services/display-service.js";

const contentImageInput = document.getElementById('content-image-input');
const contentImage = document.getElementById('content-image');
const styleImage = document.getElementById('style-image');

const artistAccordion = document.getElementById('artist-accordion');

const applyStyleButton = document.getElementById('apply-style-button');
const downloadButton = document.getElementById('download-button');

const homeLink = document.getElementById('home-link');
const reportLink = document.getElementById('report-link');

contentImageInput.addEventListener('change', (e) => {
    const input = e.target;

    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function(e) {
            contentImage.src = e.target.result;
            contentImage.classList.remove('hidden');
        };

        reader.readAsDataURL(input.files[0]);
    }

    showApplyStyleButton();
});

let chosenStyle;


function showApplyStyleButton() {
    if (!contentImage.classList.contains('hidden') && !styleImage.classList.contains('hidden')) {
        applyStyleButton.classList.remove('hidden');
    }
}

function loadArtists() {
    artistAccordion.innerHTML = createLoader();

    getArtists((artists) => {
        if (isEmpty(artists)) {
            artistAccordion.innerHTML = '';
            return;
        }

        artistAccordion.innerHTML = artists
            .map((entry, index) => `<div class="accordion-item">
                    <h2 class="accordion-header d-flex align-items-center">
                    <button data-artist-id="${entry.id}" 
                        class="accordion-button collapsed d-flex" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${index}" 
                        aria-expanded="false" aria-controls="collapse-${index}">
                        <span class="me-auto">${entry.name}</span>
                        
                        ${entry.genre.split(',').map((genre) => `<span class="badge rounded-pill text-bg-light ms-1">${genre}</span>`).join('')}
                    </button>
                  </h2>
                  
                  <div id="collapse-${index}" class="accordion-collapse collapse" data-bs-parent="#artist-accordion">
                    <div id="accordion-body-${entry.id}" class="accordion-body">
             
                      ${createLoader()}
                      
                    </div>              
                  </div>
                </div>`)
            .join('');
    });
}

function loadPaintings(artistId) {
    const accordionBody = document.getElementById(`accordion-body-${artistId}`);

    getPaintings(artistId, (paintings) => {
       if (isEmpty(paintings)) {
           accordionBody.innerHTML = '';
           return;
       }

       accordionBody.innerHTML = `<div class="row">
        
        ${paintings.map((painting) => `<div class="col-md-3 mt-3">
            <a href="#" data-style-path="${painting.path}">
                <img src="${BASE_URL}${painting.path}" class="img-thumbnail">
            </a>
        </div>`).join('')}       
       </div>`;
    });
}

artistAccordion.addEventListener('click', (e) => {
    if (e.target.tagName !== 'BUTTON') return;

    loadPaintings(e.target.dataset.artistId);
});

artistAccordion.addEventListener('click', (e) => {
    if (e.target.tagName !== 'IMG') return;

    chosenStyle = e.target.parentElement.dataset.stylePath;

    styleImage.src = e.target.src;
    styleImage.classList.remove('hidden');

    window.scroll(0, 0);

    showApplyStyleButton();
});

function createLoader() {
    return `<div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
        </div>
    </div>`;
}

applyStyleButton.addEventListener('click', (event) => {
    downloadButton.classList.add('hidden');

    const resultImageContainer = document.getElementById('result-image-container');
    resultImageContainer.innerHTML = `<p class="mt-2">
            Pablo is painting...
        </p>`;
    resultImageContainer.innerHTML += createLoader();

    applyStyle(chosenStyle);
});

homeLink.addEventListener('click', (event) => {
    event.preventDefault();
    reportLink.classList.remove('active');
    homeLink.classList.add('active');
    showApplyStyleSection();
})

reportLink.addEventListener('click', (event) => {
    event.preventDefault();
    homeLink.classList.remove('active');
    reportLink.classList.add('active');
    showReportSection();
})

hideAllSections();
loadArtists();

showApplyStyleSection();
