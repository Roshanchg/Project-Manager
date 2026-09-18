import type { BoardColor } from './types';

export const BOARD_COLORS: BoardColor[] = [
	{ name: 'blue', from: '#93c5fd', to: '#60a5fa' },
	{ name: 'teal', from: '#5eead4', to: '#2dd4bf' },
	{ name: 'green', from: '#86efac', to: '#4ade80' },
	{ name: 'red', from: '#fca5a5', to: '#f87171' },
	{ name: 'pink', from: '#f9a8d4', to: '#f472b6' },
	{ name: 'violet', from: '#c4b5fd', to: '#a78bfa' },
	{ name: 'cyan', from: '#67e8f9', to: '#22d3ee' },
	{ name: 'orange', from: '#fdba74', to: '#fb923c' }
];
export function getBoardColor(id: string): BoardColor {
	let hash = 0;
	for (let i = 0; i < id.length; i++) {
		hash = (hash * 31 + id.charCodeAt(i)) | 0;
	}
	return BOARD_COLORS[Math.abs(hash) % BOARD_COLORS.length];
}
