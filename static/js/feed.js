// Caption toggle
function toggleCaption(pk) {
  var caption = document.getElementById('caption-' + pk);
  var btn = document.getElementById('see-more-' + pk);
  if (caption.classList.contains('collapsed')) {
    caption.classList.remove('collapsed');
    btn.textContent = 'See less';
  } else {
    caption.classList.add('collapsed');
    btn.textContent = 'See more';
  }
}

// Like toggle
function toggleLike(pk) {
  fetch('/post/' + pk + '/like/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' }
  }).then(r => r.json()).then(d => {
    var icon = document.getElementById('like-icon-' + pk);
    var count = document.getElementById('like-count-' + pk);
    var btn = document.getElementById('like-btn-' + pk);
    if (icon) icon.textContent = d.liked ? '❤️' : '🤍';
    if (count) count.textContent = d.like_count;
    if (btn) btn.classList.toggle('liked', d.liked);
  });
}
