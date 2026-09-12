<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { logout } from '$lib/api/auth';
	import { userStore } from '$lib/stores/user.svelte';
	import NavItem from './NavItem.svelte';

	async function handleLogout() {
		try {
			await logout();
		} catch {
			// ignore — logging out anyway
		}
		userStore.clear();
		await goto(resolve('/login'));
	}
</script>

<aside class="sidebar">
	<header class="brand">
		<span class="brand-mark">T</span>
		<span class="brand-name">Trello-ish</span>
	</header>

	<nav class="nav">
		<NavItem href="/workspace">
			{#snippet icon()}
				<svg
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M3 7l9-4 9 4-9 4-9-4z" />
					<path d="M3 12l9 4 9-4" />
					<path d="M3 17l9 4 9-4" />
				</svg>
			{/snippet}
			Workspaces
		</NavItem>

		<NavItem href="/starred" disabled={true}>
			{#snippet icon()}
				<svg
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<polygon
						points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
					/>
				</svg>
			{/snippet}
			Starred
		</NavItem>

		<NavItem href="/settings">
			{#snippet icon()}
				<svg
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<circle cx="12" cy="12" r="3" />
					<path
						d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
					/>
				</svg>
			{/snippet}
			Settings
		</NavItem>
	</nav>

	<footer class="sidebar-footer">
		<button class="logout" onclick={handleLogout}>
			<svg
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
				<polyline points="16 17 21 12 16 7" />
				<line x1="21" y1="12" x2="9" y2="12" />
			</svg>
			<span>Log Out</span>
		</button>
	</footer>
</aside>

<style>
	.sidebar {
		display: flex;
		flex-direction: column;
		background: #f8fafc;
		color: #0f172a;
		padding: 1rem 0.75rem;
		max-height: 100vh;
		min-height: 0;
		border-right: 1px solid #e2e8f0;
	}

	/* ---------- Brand ---------- */
	.brand {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		padding: 0.5rem 0.75rem 1.5rem;
	}

	.brand-mark {
		width: 2rem;
		height: 2rem;
		border-radius: 8px;
		background: #2563eb;
		color: white;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-weight: 800;
		font-size: 1rem;
		letter-spacing: -0.02em;
		box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
	}

	.brand-name {
		font-weight: 700;
		font-size: 1rem;
		color: #0f172a;
		letter-spacing: 0.01em;
	}

	/* ---------- Nav ---------- */
	.nav {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		flex: 1;
	}

	/* ---------- Footer / Logout ---------- */
	.sidebar-footer {
		border-top: 1px solid #e2e8f0;
		padding-top: 0.75rem;
		margin-top: 0.75rem;
	}

	.logout {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		width: 100%;
		padding: 0.55rem 0.75rem;
		border-radius: 6px;
		background: transparent;
		border: none;
		color: #64748b;
		font-family: inherit;
		font-size: 0.9rem;
		font-weight: 500;
		cursor: pointer;
		text-align: left;
		transition:
			background 0.15s,
			color 0.15s;
	}

	.logout svg {
		width: 1.15rem;
		height: 1.15rem;
		flex-shrink: 0;
	}

	.logout:hover {
		background: rgba(239, 68, 68, 0.08);
		color: #dc2626;
	}

	.logout:active {
		background: rgba(239, 68, 68, 0.16);
		color: #b91c1c;
	}

	.logout:focus-visible {
		outline: none;
		box-shadow: 0 0 0 2px #2563eb;
	}
</style>
