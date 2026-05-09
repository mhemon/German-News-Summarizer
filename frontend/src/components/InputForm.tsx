import { useState } from 'react';
import { AnalyzeRequest } from '../types/api';

interface InputFormProps {
  onSubmit: (request: AnalyzeRequest) => void;
  isLoading?: boolean;
}

export function InputForm({ onSubmit, isLoading = false }: InputFormProps) {
  const [input, setInput] = useState('');
  const [summaryLength, setSummaryLength] = useState<'short' | 'medium' | 'detailed'>('medium');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    onSubmit({
      input: input.trim(),
      mode: 'auto',
      summary_length: summaryLength,
    });
  };

  const handleExample = () => {
    const exampleText = `Die deutsche Wirtschaft ist im vierten Quartal 2024 überraschend stabil geblieben. 
Trotz globaler Herausforderungen verzeichnet das Bruttoinlandsprodukt ein Wachstum von 1,5%. 
Experten führen dies auf langfristige Investitionen und den Aufschwung im Exportsektor zurück. 
Die Beschäftigung bleibt auf hohem Niveau, wobei die Arbeitslosenquote unter 4% liegt.`;
    
    setInput(exampleText);
    
    // Automatically submit the example
    setTimeout(() => {
      onSubmit({
        input: exampleText.trim(),
        mode: 'auto',
        summary_length: summaryLength,
      });
    }, 0);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-2">
          Article URL or Text
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste a German news article URL or text here..."
          className="w-full h-36 p-4 border border-slate-300 bg-white rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 resize-none transition"
          disabled={isLoading}
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-2">
          Summary Length
        </label>
        <select
          value={summaryLength}
          onChange={(e) => setSummaryLength(e.target.value as 'short' | 'medium' | 'detailed')}
          className="w-full p-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 bg-white transition"
          disabled={isLoading}
        >
          <option value="short">Short</option>
          <option value="medium">Medium</option>
          <option value="detailed">Detailed</option>
        </select>
      </div>

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-slate-400 disabled:to-slate-400 text-white font-semibold py-3 px-4 rounded-xl transition shadow-sm"
        >
          {isLoading ? 'Analyzing...' : 'Analyze Article'}
        </button>
        <button
          type="button"
          onClick={handleExample}
          disabled={isLoading}
          className="px-4 py-3 bg-slate-100 hover:bg-slate-200 disabled:bg-slate-300 text-slate-900 font-semibold rounded-xl transition"
        >
          Load Example
        </button>
      </div>
    </form>
  );
}
