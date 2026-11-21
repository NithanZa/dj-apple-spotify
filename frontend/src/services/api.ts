export type Health = { status: string; service: string }

export async function getHealth(): Promise<Health> {
  const response = await fetch('/api/health')
  if (!response.ok) throw new Error(`Health check failed: ${response.status}`)
  return response.json()
}
