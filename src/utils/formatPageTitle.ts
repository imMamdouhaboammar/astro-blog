/** Keep the site title in browser tabs and social metadata exactly once. */
export function formatPageTitle(title: string, siteTitle: string): string {
  const suffix = ` | ${siteTitle}`;
  return title === siteTitle || title.endsWith(suffix)
    ? title
    : `${title}${suffix}`;
}
