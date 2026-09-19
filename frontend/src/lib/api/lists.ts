// src/lib/mock/boardData.ts
import type { ListInfo, CardDetails } from '$lib/types';

export const mockLists: ListInfo[] = [
	{
		id: 'list-1',
		name: 'Backlog',
		position: 0,
		cards: [
			{
				id: 'card-1',
				name: 'Design database schema',
				severity: 'Low',
				tag: 'backend',
				due_date: '2026-10-05T12:00:00Z'
			},
			{
				id: 'card-2',
				name: 'Write API docs',
				severity: 'Low',
				tag: 'docs',
				due_date: '2026-10-20T12:00:00Z'
			}
		]
	},
	{
		id: 'list-2',
		name: 'In Progress',
		position: 1,
		cards: [
			{
				id: 'card-3',
				name: 'Build auth flow',
				severity: 'High',
				tag: 'backend',
				due_date: '2026-09-28T12:00:00Z'
			},
			{
				id: 'card-4',
				name: 'Board page: kanban layout',
				severity: 'Medium',
				tag: 'frontend',
				due_date: '2026-10-02T12:00:00Z'
			}
		]
	},
	{
		id: 'list-3',
		name: 'Review',
		position: 2,
		cards: [
			{
				id: 'card-5',
				name: 'Workspace CRUD',
				severity: 'Low',
				tag: 'frontend',
				due_date: '2026-09-20T12:00:00Z'
			}
		]
	},
	{
		id: 'list-4',
		name: 'Done',
		position: 3,
		cards: [
			{
				id: 'card-6',
				name: 'Project scaffolding',
				severity: 'Low',
				tag: 'setup',
				due_date: '2026-09-10T12:00:00Z'
			}
		]
	},
	{
		id: 'list-5',
		name: 'Archive',
		position: 4,
		cards: []
	}
];

export const mockCardDetails: Record<string, CardDetails> = {
	'card-1': {
		id: 'card-1',
		desc: 'Tables for users, workspaces, boards, lists, cards, checklists.',
		checklist: [
			{
				id: 'cl-1',
				name: 'Schema',
				items: [
					{ id: 'ci-1', val: 'Users table', position: 0, checked: true, checked_by: 'user-1' },
					{ id: 'ci-2', val: 'Workspaces table', position: 1, checked: true, checked_by: 'user-1' },
					{
						id: 'ci-3',
						val: 'Membership join table',
						position: 2,
						checked: false,
						checked_by: null
					},
					{ id: 'ci-4', val: 'Indexes on FKs', position: 3, checked: false, checked_by: null }
				]
			}
		]
	},

	'card-2': {
		id: 'card-2',
		desc: null,
		checklist: []
	},

	'card-3': {
		id: 'card-3',
		desc: 'JWT access + refresh tokens in httpOnly cookies.',
		checklist: [
			{
				id: 'cl-2',
				name: 'Backend',
				items: [
					{
						id: 'ci-5',
						val: 'Register endpoint',
						position: 0,
						checked: true,
						checked_by: 'user-1'
					},
					{ id: 'ci-6', val: 'Login endpoint', position: 1, checked: true, checked_by: 'user-1' },
					{ id: 'ci-7', val: 'Refresh endpoint', position: 2, checked: false, checked_by: null },
					{ id: 'ci-8', val: 'Logout endpoint', position: 3, checked: false, checked_by: null }
				]
			},
			{
				id: 'cl-3',
				name: 'Frontend',
				items: [
					{ id: 'ci-9', val: 'Login page', position: 0, checked: true, checked_by: 'user-1' },
					{ id: 'ci-10', val: 'Register page', position: 1, checked: true, checked_by: 'user-1' },
					{
						id: 'ci-11',
						val: 'Auth guard on layout',
						position: 2,
						checked: false,
						checked_by: null
					}
				]
			}
		]
	},

	'card-4': {
		id: 'card-4',
		desc: 'Horizontal scroll of lists, vertical card stacks.',
		checklist: []
	},

	'card-5': {
		id: 'card-5',
		desc: null,
		checklist: [
			{
				id: 'cl-4',
				name: 'QA',
				items: [
					{ id: 'ci-12', val: 'Create flow', position: 0, checked: true, checked_by: 'user-2' },
					{ id: 'ci-13', val: 'Edit flow', position: 1, checked: true, checked_by: 'user-2' },
					{ id: 'ci-14', val: 'Delete flow', position: 2, checked: true, checked_by: 'user-2' },
					{ id: 'ci-15', val: 'Empty state copy', position: 3, checked: false, checked_by: null }
				]
			}
		]
	},

	'card-6': {
		id: 'card-6',
		desc: 'FastAPI + SvelteKit, dev proxy, static adapter.',
		checklist: [
			{
				id: 'cl-5',
				name: 'Setup',
				items: [
					{
						id: 'ci-16',
						val: 'Create FastAPI project',
						position: 0,
						checked: true,
						checked_by: 'user-1'
					},
					{
						id: 'ci-17',
						val: 'Create SvelteKit project',
						position: 1,
						checked: true,
						checked_by: 'user-1'
					},
					{
						id: 'ci-18',
						val: 'Configure Vite proxy',
						position: 2,
						checked: true,
						checked_by: 'user-1'
					}
				]
			}
		]
	}
};
