<script lang="ts">
	import type { BoardInfo } from '$lib/types';
    import {  getBoardColor } from '$lib/boardColors';
	import { page } from '$app/state';
	// import { resolve } from '$app/paths';



	type Props = {
		board: BoardInfo;
		onEdit?: (board: BoardInfo) => void;
		onDelete?: (board: BoardInfo) => void;
	};
	let { board, onEdit, onDelete }: Props = $props();

	let menuEl = $state<HTMLDetailsElement | null>(null);
	let workspaceId=$derived(page.params.id);
	function menuClose() {
		if (menuEl) menuEl.open = false;
	}
	function handleEdit(e: MouseEvent) {
		e.stopPropagation();
		e.preventDefault();
		menuClose();
		onEdit?.(board);
	}
	function handleDelete(e: MouseEvent) {
		e.stopPropagation();
		e.preventDefault();
		menuClose();
		onDelete?.(board);
	}
</script>

<a
	class="board-card"
	// eslint-disable-next-line svelte/no-navigation-without-resolve
	href={`/workspace/${workspaceId}/boards/${board.id}`}
	style:--colorFrom={getBoardColor(board.id).from}
    style:--colorTo={getBoardColor(board.id).to}
>
	<div class="header">
		<strong class="name">{board.name}</strong>
		<details aria-label="more options" class="menu" bind:this={menuEl}>
			<summary
				onclick={(e: MouseEvent) => {
					e.stopPropagation();
				}}
			>
				<svg
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
			</summary>
			<div class="menu-panel">
				<button onclick={handleEdit} aria-label="edit"
					><svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-6"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
						/>
					</svg>
				</button>
				<button onclick={handleDelete} aria-label="delete">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-6"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
						/>
					</svg>
				</button>
			</div>
		</details>
	</div>
	<div class="footer">
		<span class="card-amount-label">Total Cards: </span>
        <span class="card-amount-value">{board.totalCards}</span>
	</div>
</a>

<style>
	.board-card {
		text-decoration: none;
		color: black;
		padding: 1.5em;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-height: 90px;
		border-radius: 16px;
		background: linear-gradient(135deg, 
			color-mix(in srgb, var(--colorFrom) 60%, transparent) 0%,

		 	color-mix(in srgb, var(--colorTo) 60%, transparent) 60%);
		box-shadow: inset 0px 4px 12px var(--colorFrom);
	}
	.name {
		font-size: 18px;
	}

	.header {
		display: flex;
		align-items: center;
		position: relative;
		justify-content: space-between;
	}
	.menu {
		outline: none;
		background-color: transparent;
		border: none;
		cursor: pointer;
		> summary {
			list-style: none;
		}
		.menu-panel {
			position: absolute;
			top: calc(100% + 0.2rem);
			left: calc(100% - 0.8rem);
			right: 0;
			background: white;
			border: 1px solid #e2e8f0;
			border-radius: 8px;
			box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15);
			padding: 0.25rem;
			width: fit-content;
			z-index: 20;
			display: flex;
			flex-direction: column;
			> button {
				display: block;
				width: 100%;
				text-align: left;
				padding: 0.5rem 0.75rem;
				border: none;
				background: transparent;
				border-radius: 6px;
				font-family: inherit;
				font-size: 0.9rem;
				color: #334155;
				cursor: pointer;
				transition: background 0.1s;
				> svg {
					width: 20px;
					height: 20px;
				}
			}
			>button:hover{
				background-color: #C7DAFA;
			}
		}
	}
	.menu > summary > svg {
		fill: black;
	}
	.footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		position: relative;
		.card-amount-label{
			font-style: italic;
		}
		.card-amount-value{
			font-weight: 550;
		}
	}
	
</style>
