<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { me } from '$lib/api/auth';
	import { ApiError } from '$lib/api/client';
	import { userStore } from '$lib/stores/user.svelte';
	import type { User } from '$lib/types';
	import { onMount } from 'svelte';

	import Topbar from '$lib/components/layout/Topbar.svelte';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';

	let { children } = $props();

	let user = $state<User | null>(null);
	let checking = $state(true);
	onMount(async () => {
		try {
			userStore.setLoading(true);
			user = await me();
			userStore.set(user);
		} catch (err) {
			if (err instanceof ApiError && err.status != 401) {
				console.error('Auth check failed', err);
			}
			await goto(resolve('/login'));
			return;
		} finally {
			checking = false;
			userStore.setLoading(false);
		}
	});
</script>

{#if checking}
	<div class="guard-loading">Loading...</div>
{:else if userStore.user}
	<div class="shell">
		<Sidebar />
		<div class="right">
			<Topbar />
			<main class="content">
				{@render children()}
			</main>
		</div>
	</div>
{/if}

<style>
	.guard-loading {
		min-height: 100vh;
		display: grid;
		place-items: center;
		font-family: system-ui, sans-serif;
		color: #5e6c84;
	}

	.shell {
		display: grid;
		grid-template-columns: minmax(220px, 12%) minmax(0, 1fr);
		height: 100vh;
		padding: 0;
		margin: 0;
		overflow: hidden;
	}
	.content {
		padding: 1.4em;
		overflow-y: auto;
		overflow-x: hidden;
	}
	.right {
		height: 100vh;
		min-height: 0;
		display: flex;
		flex-direction: column;
	}
</style>
