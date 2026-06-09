import { AnalyzeRequest, AnalyzeResponse } from '../types/api';

export const API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');

const REQUEST_TIMEOUT_MS = 30000;

async function fetchWithTimeout(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    return await fetch(input, {
      ...init,
      signal: controller.signal,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new Error('Request timed out. Please check that the backend is running and try again.');
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function analyzeArticle(request: AnalyzeRequest): Promise<AnalyzeResponse> {
  const response = await fetchWithTimeout(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to analyze article');
  }

  return response.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetchWithTimeout(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error('Health check failed');
  }
  return response.json();
}
