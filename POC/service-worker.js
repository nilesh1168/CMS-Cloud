self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('appCache').then(function(cache) {
      return cache.addAll(
        [
          // '/static/js/jquery-3.4.1.min.js',
          // '/static/css/simple-sidebar.css',
          // '/static/css/cert1.jpg',
          // '/static/js/getdata.js',
          // '/static/js/notification.js',
          // '/static/js/sidebar_menu.js',
          // '/static/js/studentdetail.js'
        ]
      );
    })
  );
});

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