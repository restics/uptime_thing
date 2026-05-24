function StatusCard({card}) {

  return (
    <div>
        <h2>{card.name}</h2>
        <p>{card.description}</p>
        <p>{card.url}</p>
        <p>{card.status}</p>
        <p>{card.latency}ms</p>
    </div>
  )
}

export default StatusCard