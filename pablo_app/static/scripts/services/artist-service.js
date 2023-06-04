import {ARTISTS_URL, PAINTINGS_URL, TRANSFER_URL} from "../utils/constants.js";

async function fetchArtists() {
    return await (await fetch(ARTISTS_URL, {mode: 'cors'})).json();
}

async function fetchPaintings(artistId) {
    return await (await fetch(PAINTINGS_URL(artistId))).json();
}

async function postApplyStyle(chosenStyle) {
    let formData = new FormData();
    formData.append('file', document.getElementById('content-image-input').files[0]);
    formData.append('style', chosenStyle);

    fetch(TRANSFER_URL, {
        method: 'POST',
        body: formData
    })
        .then(res => {
            console.log(res);
            return res.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);

            const resultImageContainer = document.getElementById('result-image-container');
            resultImageContainer.innerHTML = `<img class="img-fluid img-thumbnail" src=${url} alt="">`;

            const downloadLink = document.getElementById('download-button');
            downloadLink.classList.remove('hidden');
            downloadLink.download = 'pablos_painting.png';
            downloadLink.href = url;

        })
        .catch(err => {
            console.log(err);
        });
}

export function getArtists(artistsCallbackHandlerFunction) {
    fetchArtists()
        .then((artistsArray) => artistsCallbackHandlerFunction(artistsArray));
}

export function getPaintings(artistId, paintingsCallbackHandlerFunction) {
    fetchPaintings(artistId)
        .then((paintingsArray) => paintingsCallbackHandlerFunction(paintingsArray));
}

export function applyStyle(chosenStyle) {
    postApplyStyle(chosenStyle).then(r => r);
}
