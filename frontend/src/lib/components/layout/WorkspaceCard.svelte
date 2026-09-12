<script lang="ts">
	import type { WorkspaceInfo } from '$lib/types';

	type Props={workspace:WorkspaceInfo}
	let { workspace }:Props = $props();
</script>

<div class="workspace-card" style:--color={workspace.color}>
	<div class="header">
		<strong class="name">{workspace.name}</strong>
		<button aria-label="more options" class="menu"
			><svg
				xmlns="http://www.w3.org/2000/svg"
				fill="#00000044"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				width="24px"
				height="24px"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"
				/>
			</svg>
		</button>
	</div>
	<div class="footer">
		<details class="user-menu">
			<summary class="trigger">
				<span class="avatar">{workspace.owner.charAt(0).toUpperCase()}</span>
			</summary>

			<div class="panel">
				<div class="info">
					<strong>{workspace.owner}</strong>
				</div>
			</div>
		</details>
		<code><strong>{workspace.role}</strong></code>
	</div>
</div>

<style>
	.workspace-card {
		background-color: var(--color);
		padding: 1.5em;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-height: 90px;
		height: 120px;
		border-radius: 16px;
		box-shadow: 4px 4px 18px var(--color);
	}
	.name {
		font-size: 18px;
	}

	.header {
		display: flex;
		align-items: center;

		justify-content: space-between;
	}
	.menu {
		outline: none;
		background-color: transparent;
		border: none;
		cursor: pointer;
	}
	.menu > svg {
		fill: black;
	}
	.footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		position: relative;
	}
	.trigger {
		list-style: none;
		background: #0052cc;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 4px 4px 12px #00000032;
	}
	.trigger:active {
		box-shadow: none;
	}
	.avatar {
		color: white;
		font-weight: bold;
		font-size: 16px;
	}
	.panel {
		position: absolute;
		background-color: #ffffff;
		padding: 0.5em 1em;
		border: 1px solid #dfe1e6;
		top: calc(100% + 0.4rem);
		left: 10px;
		z-index: 10;
		cursor: text;
		border-radius: 8px;
		box-shadow: 0px 4px 12px #dfe1e6;
	}
	code {
		padding: 2px 6px;
		border-radius: 4px;
		text-align: center;
		border: 1px solid #dedede;
		background-color: white;
		color: rgb(42, 126, 209);
		display: flex;
		align-items: center;
		justify-content: center;
		> strong {
			font-size: 16px;
		}
	}
</style>
