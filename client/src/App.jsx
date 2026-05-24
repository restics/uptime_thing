import { useState, useEffect } from 'react'
import StatusCard from './StatusCard'

function App() {
  const [cards, setCards] = useState([])
  const [form, setForm] = useState({
    name: '',
    url: '',
    description: ''
  })
  useEffect(() => {
    const fetchCards = () => {
      fetch('${import.meta.env.VITE_API_URL}/cards')
          .then(res => res.json())
          .then(data => setCards(data))
    }

    fetchCards() // run immediately on mount
    const interval = setInterval(fetchCards, 5000) // then every 5s

    return () => clearInterval(interval)
  }, [])

  async function handleSubmit(){

    await fetch('${import.meta.env.VITE_API_URL}/cards/create', {
      method: 'POST', 
      headers: {
      'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)
    })
  
    fetch('${import.meta.env.VITE_API_URL}/cards')
        .then(res => res.json())
        .then(data => setCards(data))
  }

  
  return (
    <div>
      <h1>Uptime Monitor</h1>
      <div>
        <h2>Create Card</h2>
        <input
          value = {form.name}
          onChange = {e => setForm({ ...form, name: e.target.value})}
          placeholder='Name'
        />
        <input
          value = {form.url}
          onChange = {e => setForm({ ...form, url: e.target.value})}
          placeholder='Url'
        />
        <input
          value = {form.description}
          onChange = {e => setForm({ ...form, description: e.target.value})}
          placeholder='Description'
        />
        <button onClick={handleSubmit}>submit</button>
      </div>
      {cards.map(card => (
        <StatusCard key={card.id} card={card} />
      ))}
    </div>
  )
}



export default App