export function renderDate(value: string) {
  const datetime = new Date(value);
  const date = `${datetime.getDate()}.${datetime.getMonth()}.${datetime.getFullYear()}`;
  const time = `${datetime.getHours()}:${datetime.getMinutes()}`;
  return `${date} - ${time}`;
}
