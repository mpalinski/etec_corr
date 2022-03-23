window.addEventListener('load', () => {

            parent.postMessage(JSON.stringify({ event_id: 'handshake', data: { height: document.body.scrollHeight } }), '*');

            function onResize() {
                parent.postMessage(JSON.stringify({ event_id: 'resized', data: { height: document.body.scrollHeight } }), '*');
            }

            window.addEventListener('resize', onResize, false);
        })
