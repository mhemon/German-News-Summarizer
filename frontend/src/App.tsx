import { useState, useEffect } from 'react';
import { InputForm } from './components/InputForm';
import { ResultsCard } from './components/ResultsCard';
import { analyzeArticle, healthCheck } from './lib/api';
import { AnalyzeRequest, AnalyzeResponse } from './types/api';

function App() {
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check if backend is available
    healthCheck()
      .then(() => setIsConnected(true))
      .catch(() => setIsConnected(false));
  }, []);

  const handleAnalyze = async (request: AnalyzeRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await analyzeArticle(request);
      setResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(1200px_500px_at_20%_-10%,#dbeafe_0%,transparent_60%),radial-gradient(1000px_500px_at_100%_0%,#cffafe_0%,transparent_55%),linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)]">
      {/* Header */}
      <header className="border-b border-slate-200/70 bg-white/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900">German News Summarizer by Emon</h1>
          <p className="text-slate-600 mt-2 text-lg">
            Summarize German news articles in German and English
          </p>
          {!isConnected && (
            <div className="mt-4 inline-flex items-center gap-2 px-3 py-2 bg-amber-50 border border-amber-300 rounded-full text-amber-800 text-sm">
              ⚠️ Backend connection unavailable. Please ensure the backend server is running on port 8000.
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Section */}
          <div className="lg:col-span-1">
            <div className="bg-white/90 rounded-2xl shadow-lg border border-slate-200 p-6 sticky top-6">
              <h2 className="text-lg font-bold text-slate-900 mb-4">Input</h2>
              <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            <ResultsCard data={results} isLoading={isLoading} error={error} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
