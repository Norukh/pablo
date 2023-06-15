export const BASE_URL = ""
export const SERVICE_URL = `${BASE_URL}/`;

export const ARTISTS_URL = `${SERVICE_URL}artists`;
export const PAINTINGS_URL = (artistId) => `${SERVICE_URL}paintings/${artistId}`;
export const TRANSFER_URL = `${SERVICE_URL}transfer`;
