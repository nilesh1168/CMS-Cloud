self.addEventListener('install', event => {event.waitUntil(self.skipWaiting())});


self.addEventListener('activate', event => {
event.waitUntil(self.clients.claim())
	console.log('Ready!');
});


self.addEventListener("message",function (event) {
  console.log(event.data);
  event.source.postMessage("From ServiceWorker.js")
  });



self.addEventListener('notificationclick',function (event) {
  console.log("inside notification click!!");
  console.log(this);
  console.log(event.notification.tag);
  clients.matchAll().then(clients => {
    clients.forEach(
      client => client.postMessage({msg: 'Hello from SW', tag : event.notification.tag})
      );
      
  })
  event.notification.close();
}); 