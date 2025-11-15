export default function Header() {
  return (
    <header className="header-gradient rounded-xl p-4 text-white shadow-lg">
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded bg-white/10 flex items-center justify-center text-2xl">
          🛡️
        </div>
        <div>
          <div className="text-2xl font-bold">IoT Guardian</div>
          <div className="text-sm opacity-90">Cyber Blue Dashboard</div>
        </div>
      </div>
    </header>
  );
}

