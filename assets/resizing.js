window.addEventListener('load', () => {

            parent.postMessage(JSON.stringify({ event_id: 'handshake', data: { height: document.querySelector('#dash').scrollHeight } }), '*');

            function onResize() {
                parent.postMessage(JSON.stringify({ event_id: 'resized', data: { height: document.querySelector('#dash').scrollHeight } }), '*');
            }

            window.addEventListener('resize', onResize, false);
        })
