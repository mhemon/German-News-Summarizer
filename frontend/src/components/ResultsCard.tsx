import { AnalyzeResponse } from '../types/api';

interface ResultsCardProps {
  data: AnalyzeResponse | null;
  isLoading?: boolean;
  error?: string | null;
}

export function ResultsCard({ data, isLoading = false, error = null }: ResultsCardProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing article...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
        <h3 className="text-red-900 font-semibold mb-2">Error</h3>
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>Submit an article to see results</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Article Info */}
      <div className="bg-white/95 rounded-2xl border border-slate-200 p-6 shadow-sm">
        <h2 className="text-3xl font-extrabold tracking-tight text-slate-900 mb-2">{data.title}</h2>
        <p className="text-slate-600 mb-4 text-lg">
          <span className="font-semibold">{data.source}</span> • {data.reading_time_minutes} min read
        </p>
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 max-h-44 overflow-hidden">
          <p className="text-slate-700 text-base line-clamp-6">{data.article_text}</p>
        </div>
      </div>

      {/* Summaries */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h3 className="text-2xl font-bold text-slate-900 mb-3">German Summary</h3>
          <p className="text-slate-700 leading-relaxed text-[1.1rem]">{data.german_summary}</p>
          <button className="mt-4 text-sm text-blue-600 hover:text-blue-800 font-semibold">
            Copy Summary
          </button>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h3 className="text-2xl font-bold text-slate-900 mb-3">English Summary</h3>
          <p className="text-slate-700 leading-relaxed text-[1.1rem]">{data.english_summary}</p>
          <button className="mt-4 text-sm text-blue-600 hover:text-blue-800 font-semibold">
            Copy Summary
          </button>
        </div>
      </div>

      {/* Keywords and Entities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-3">Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {data.keywords.map((keyword) => (
              <span
                key={keyword}
                className="px-3 py-1 bg-cyan-100 text-cyan-800 text-sm rounded-full font-medium"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-3">People</h3>
          <ul className="space-y-1">
            {data.entities.people.map((person) => (
              <li key={person} className="text-sm text-slate-700">
                • {person}
              </li>
            ))}
          </ul>
          {data.entities.people.length === 0 && <p className="text-sm text-slate-500">None found</p>}
        </div>
      </div>

      {/* Tone and Details */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-slate-600 font-medium">Tone</p>
            <p className="text-lg font-semibold text-slate-900 capitalize">{data.tone}</p>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Language</p>
            <p className="text-lg font-semibold text-slate-900">{data.language.toUpperCase()}</p>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Reading Time</p>
            <p className="text-lg font-semibold text-slate-900">{data.reading_time_minutes} min</p>
          </div>
        </div>
      </div>
    </div>
  );
}
