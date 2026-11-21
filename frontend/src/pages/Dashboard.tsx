import { useEffect, useState } from 'react'
import { getHealth } from '../services/api'

type BackendState = 'checking' | 'online' | 'offline'

export default function Dashboard() {
  const [backend, setBackend] = useState<BackendState>('checking')

  useEffect(() => {
    getHealth()
      .then(() => setBackend('online'))
      .catch(() => setBackend('offline'))
  }, [])

  return (
    <main>
      <h1>Rekordbox Migrator</h1>
      <p>Backend: {backend}</p>
    </main>
  )
}
