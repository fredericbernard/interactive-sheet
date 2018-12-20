const serverUrl = "http://localhost:4000"

export function getDrawing() {
  return fetch(`${serverUrl}/drawing`).then(res => res.json());
}

export function clearDrawing() {
  return fetch(`${serverUrl}/drawing/clear`, {method: 'post'});
}

export function addLine(start_x, start_y, end_x, end_y) {
  return fetch(`${serverUrl}/drawing`, {
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      start: [
        start_x, start_y
      ],
      end: [end_x, end_y]
    })
  });
}

export function lock() {
  return fetch(`${serverUrl}/drawing/lock`, {method: 'post'})
}


export function unlock() {
  return fetch(`${serverUrl}/drawing/unlock`, {method: 'post'})
}

export function isLocked() {
  return fetch(`${serverUrl}/drawing/lock`).then(res => res.json()).then(res => res.locked);
}
