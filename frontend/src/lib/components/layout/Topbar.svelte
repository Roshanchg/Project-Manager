<script lang="ts">
	import { userStore } from '$lib/stores/user.svelte';
	import UserMenu from './UserMenu.svelte';

	let searchQuery = $state('');
</script>

<header class="topbar">
	<div class="left">
		<input
			class="search"
			type="search"
			placeholder="Search (coming soon)"
			bind:value={searchQuery}
			disabled
		/>
	</div>

	<div class="right">
		<button class="icon-btn" type="button" aria-label="Notifications">
			<svg
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9" />
				<path d="M13.7 21a2 2 0 01-3.4 0" />
			</svg>
		</button>

		{#if userStore.user}
			<UserMenu user={userStore.user} />
		{/if}
	</div>
</header>

<style>
	.topbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.75rem 1.25rem;
		background: white;
		border-bottom: 1px solid #dfe1e6;
		height: 40px;
		flex-shrink: 0;
	}

	.left {
		flex: 1;
		max-width: 800px;
	}

	.search {
		width: 100%;
		padding: 0.5rem 0.75rem;
		border: 1px solid #dfe1e6;
		border-radius: 6px;
		font-family: inherit;
		font-size: 0.9rem;
		background: #f4f5f7;
	}

	.search:disabled {
		cursor: not-allowed;
		opacity: 0.7;
	}

	.right {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.icon-btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 2rem;
		height: 2rem;
		border-radius: 6px;
		background: transparent;
		border: none;
		color: #42526e;
		cursor: pointer;
		transition: background 0.15s;
	}

	.icon-btn:hover {
		background: #f4f5f7;
	}

	.icon-btn svg {
		width: 1.15rem;
		height: 1.15rem;
	}
</style>
