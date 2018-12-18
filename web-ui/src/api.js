const serverUrl = "http://localhost:4000"

export function getDrawing() {
  return fetch(`${serverUrl}/drawing`).then(res => res.json());
}

export function clearDrawing() {
  return fetch(`${serverUrl}/drawing/clear`, {method: 'post'});
}
