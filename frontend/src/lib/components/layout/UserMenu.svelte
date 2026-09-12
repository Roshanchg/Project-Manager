<script lang="ts">
	import type { User } from '$lib/types';

	type Props = { user: User };
	let { user }: Props = $props();
</script>

<details class="user-menu">
	<summary class="trigger">
		<span class="avatar">{user.full_name.charAt(0).toUpperCase()}</span>
	</summary>

	<div class="panel">
		<div class="info">
			<strong>{user.full_name}</strong>
			<span>{user.email}</span>
		</div>
	</div>
</details>

<style>
	.user-menu {
		position: relative;
	}

	.trigger {
		list-style: none;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.15rem;
		border-radius: 50%;
		outline: none;
	}

	.trigger::-webkit-details-marker {
		display: none;
	}

	.trigger:focus-visible {
		box-shadow: 0 0 0 2px #4c9aff;
	}

	.avatar {
		width: 2rem;
		height: 2rem;
		border-radius: 50%;
		background: #0052cc;
		color: white;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		font-size: 0.9rem;
		user-select: none;
	}

	.panel {
		position: absolute;
		top: calc(100% + 0.5rem);
		right: 0;
		background: white;
		border: 1px solid #dfe1e6;
		border-radius: 8px;
		box-shadow: 0 8px 24px rgba(9, 30, 66, 0.15);
		padding: 0.75rem 1rem;
		min-width: 220px;
		z-index: 10;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}

	.info strong {
		color: #172b4d;
		font-size: 0.9rem;
	}

	.info span {
		color: #5e6c84;
		font-size: 0.8rem;
		word-break: break-all;
	}
</style>
