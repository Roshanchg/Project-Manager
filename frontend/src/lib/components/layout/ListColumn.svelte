<script lang="ts">
	import { mockCardDetails } from '$lib/api/lists';
	import type { CardInfo, ListInfo } from '$lib/types';
	import CardCard from './CardCard.svelte';

	type Props = {
		list: ListInfo;
		onEdit?: (list: ListInfo) => void;
		onDelete?: (list: ListInfo) => void;
	};

	let { list, onEdit, onDelete }: Props = $props();

	let listMenu = $state<HTMLDetailsElement | null>(null);
	let listEl = $state<HTMLDetailsElement | null>(null);

	function handleEdit(e: MouseEvent) {
		e.stopPropagation();
		listMenuClose();
		onEdit?.(list);
	}
	function handleDelete(e: MouseEvent) {
		e.stopPropagation();
		listMenuClose();
		onDelete?.(list);
	}

	function listMenuClose() {
		if (listMenu) listMenu.open = false;
	}

	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	function getCardDetails(card: CardInfo) {

		return mockCardDetails[0];
	}
	// function toggleList(){
	//     if (listEl) {listEl.open=!listEl.open};
	// }
</script>

<details bind:this={listEl} class="main-detail" open={true}>
	<summary class="list-summary">
		<h1>{list.name}</h1>
		<details class="extra-detail" open={false}>
			<summary
				onclick={(e: MouseEvent) => {
					e.stopPropagation();
				}}
				class="menu-summary"
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
			<div class="panel">
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
					</svg></button
				>
				<button onclick={handleDelete} aria-label="delete"
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
							d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
						/>
					</svg></button
				>
			</div>
		</details>
	</summary>
	<ul class="card-lists">
		{#if list.cards.length > 0}
			{#each list.cards as card (card.id)}
				<li class="card-li">
					<CardCard {card} getDetails={getCardDetails} />
				</li>
			{/each}
		{:else}
			<li class="no-items">NO ITEMS FOUND</li>
		{/if}

		<button class="new-card-btn"> Insert New Card </button>
	</ul>
</details>

<style>
	.main-detail {
		position: relative;
		background-color: #eff6ff;
		min-width: 360px;
		width: 360px;
		box-sizing: border-box;
		padding: 0.8em 1em 1.4em 1em;
		height: max-content;
		border-radius: 12px;
	}
	.list-summary {
		display: flex;
		align-items: center;
		justify-content: space-between;

		> h1 {
			margin: 0;
			font-size: 1rem;
			font-weight: 600;
		}
	}

	.menu-summary {
		list-style: none;
		cursor: pointer;
	}
	.panel {
		position: absolute;
		display: flex;
		flex-direction: column;
		left: 94%;
		border: 2px solid #e2e2e2;
		border-radius: 12px;
		background-color: #ffffff;
		padding: 4px 2px;
		> button {
			box-sizing: border-box;
			background-color: transparent;
			outline: none;
			width: 32px;
			height: 32px;
			border: none;
			cursor: pointer;
			border-radius: 12px;
		}
		> button:hover {
			background-color: #cfe9fc;
		}
	}
	ul {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	li {
		list-style: none;
		width: 100%;
	}
	.no-items {
		display: flex;
		text-align: center;
		align-items: center;
		justify-content: center;
		font-weight: 550;
	}
	.new-card-btn {
		height: 34px;
		border-radius: 8px;
		background-color: #0051b8cc;
		color: white;
		font-weight: 550;
		border: 1px solid #0051b8;
		cursor: pointer;
	}
</style>
