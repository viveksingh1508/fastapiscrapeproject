function timeAgo(dateString) {
  const now = new Date();
  const posted = new Date(dateString);
  const diffMs = now - posted;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);
  const diffWeek = Math.floor(diffDay / 7);
  const diffMonth = Math.floor(diffDay / 30);

  if (diffMonth > 0) {
    return `Posted ${diffMonth} ${diffMonth === 1 ? "month" : "months"} ago`;
  } else if (diffWeek > 0) {
    return `Posted ${diffWeek} ${diffWeek === 1 ? "week" : "weeks"} ago`;
  } else if (diffDay > 0) {
    return `Posted ${diffDay} ${diffDay === 1 ? "day" : "days"} ago`;
  } else if (diffHr > 0) {
    return `Posted ${diffHr} ${diffHr === 1 ? "hour" : "hours"} ago`;
  } else if (diffMin > 0) {
    return `Posted ${diffMin} ${diffMin === 1 ? "minute" : "minutes"} ago`;
  } else {
    return "Posted just now";
  }
}

document.querySelectorAll("[data-posted-at]").forEach(function (el) {
  const date = el.getAttribute("data-posted-at");
  el.textContent = timeAgo(date);
});
