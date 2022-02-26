export function renderDate(value: string) {
  const datetime = new Date(value);
  return Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  }).format(datetime);
}
