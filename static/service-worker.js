self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('conexao-paulista-cache').then(function(cache) {
      return cache.addAll([
        '/',
        '/alunos',
        '/aulas',
        '/calendario',
        '/static/style.css'
      ]);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});