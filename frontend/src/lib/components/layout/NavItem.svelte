<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import type { Snippet } from 'svelte';

	type Props = {
		href: string;
		icon: Snippet;
		children: Snippet;
		disabled?: boolean;
	};

	let { href, icon, children, disabled = false }: Props = $props();

	function handleClick() {
		// eslint-disable-next-line svelte/no-navigation-without-resolve
		goto(href);
	}
	let isActive = $derived(page.url.pathname === href);
</script>

<button type="button" class="nav-item" class:active={isActive} onclick={handleClick} {disabled}>
	<span class="icon">{@render icon()}</span>
	<span class="label">{@render children()}</span>
</button>

<style>
	.nav-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		width: 100%;
		padding: 0.55rem 0.75rem;
		border-radius: 6px;
		background: transparent;
		border: none;
		color: #475569;
		font-family: inherit;
		font-size: 0.9rem;
		font-weight: 500;
		text-align: left;
		cursor: pointer;
		transition:
			background 0.15s,
			color 0.15s;
	}
	.nav-item:disabled {
		opacity: 60%;
		cursor: not-allowed;
	}

	.nav-item:hover {
		background: rgba(37, 99, 235, 0.08);
		color: #1e293b;
	}

	.nav-item:active {
		background: rgba(37, 99, 235, 0.16);
		color: #0f172a;
	}
	.nav-item.active {
		background: rgba(20, 89, 238, 0.2);
	}
	.nav-item:focus-visible {
		outline: none;
		box-shadow: 0 0 0 2px #2563eb;
	}

	.icon {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.15rem;
		height: 1.15rem;
		flex-shrink: 0;
	}

	.icon :global(svg) {
		width: 100%;
		height: 100%;
		display: block;
	}

	.label {
		flex: 1;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>
