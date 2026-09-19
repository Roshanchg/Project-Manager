<script lang="ts">
	import { mockCardDetails } from '$lib/api/lists';
	import { type ISODateTime, type CardInfo, type CardDetails } from '$lib/types';

	type Props = {
		card: CardInfo;
		getDetails?: (card: CardInfo) => CardDetails;
	};

	let { card, getDetails }: Props = $props();

	let detailDlg = $state<HTMLDialogElement | null>(null);
	let detailName = $state<string>('');
	let detailSeverity = $state<string>('');
	let detailTag = $state<string>('');
	let detailDate = $state<ISODateTime>('');
	let cardDetails = $state<CardDetails | null>(null);

	let isLoadingDetails = $state<boolean>(false);
	function showCardDetails() {
		isLoadingDetails = true;
		console.log('Details: ', getDetails !== null);
		if (getDetails) cardDetails = getDetails?.(card);
		cardDetails = mockCardDetails['card-1'];
		detailName = card.name;
		detailSeverity = card.severity;
		detailTag = card.tag;
		detailDate = card.due_date;
	}

	function openDetails() {
		showCardDetails();
		isLoadingDetails = false;
		detailDlg?.showModal();
	}

	function handleBackdrop(e: MouseEvent) {
		if (e.target === detailDlg) detailDlg?.close();
	}
</script>

<dialog class="card-detail-dlg" bind:this={detailDlg} onclick={handleBackdrop}>
	{#if isLoadingDetails}
		<p>Loading...</p>
	{:else}
		<div class="card-detail-div">
			<div class="major-detail">
				<div class="topleft">
					<div class="detail-title">
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
								d="M3 8.25V18a2.25 2.25 0 0 0 2.25 2.25h13.5A2.25 2.25 0 0 0 21 18V8.25m-18 0V6a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 6v2.25m-18 0h18M5.25 6h.008v.008H5.25V6ZM7.5 6h.008v.008H7.5V6Zm2.25 0h.008v.008H9.75V6Z"
							/>
						</svg>
						<h1>{detailName}</h1>
					</div>

					<div class="tags">
						<span>Tags</span>
						<div>
							<code>{detailSeverity}</code>
							<code>{detailTag}</code>
						</div>
					</div>
					<div class="date">
						<span>Due Date</span>
						<label>
							<code>{detailDate}</code>
							<button>OVERDUE</button>
						</label>
					</div>
				</div>
				<div class="topright">
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
							d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"
						/>
					</svg>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-6"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
					</svg>
				</div>
			</div>
			<div class="desc-detail">
				<label class="desc-title">
					<div>
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
								d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12"
							/>
						</svg>
						<span>Description</span>
					</div>
					<button>Edit</button>
				</label>
				<p>{cardDetails?.desc}</p>
			</div>
			{#each cardDetails?.checklist as checklist (checklist.id)}
				<div class="checklist-detail">
					<label class="checklist-title">
						<div>
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
									d="M5.25 7.5A2.25 2.25 0 0 1 7.5 5.25h9a2.25 2.25 0 0 1 2.25 2.25v9a2.25 2.25 0 0 1-2.25 2.25h-9a2.25 2.25 0 0 1-2.25-2.25v-9Z"
								/>
							</svg>
							<span>{checklist.name}</span>
						</div>
						<button>Delete</button>
					</label>
					<ul class="checklist-list">
						{#each checklist.items as clItem (clItem.id)}
							<label class="checklist-item">
								<div>
									<input type="checkbox" bind:checked={clItem.checked} />
									<span>{clItem.val}</span>
								</div>
								{#if clItem.checked}
									<details class="checked-by">
										<summary>
											{clItem.checked_by?.[0].toUpperCase()}
										</summary>
										<strong>{clItem.checked_by}</strong>
									</details>
								{/if}
							</label>
						{/each}
						<button class="new-item-btn">Add an item</button>
					</ul>
				</div>
			{/each}
			<button class="new-checklist-btn">Add New Checklist</button>
		</div>
	{/if}
</dialog>

<button onclick={openDetails} class="card">
	<div class="header">
		<span class="tag-tag">{card.tag}</span>
		<span class="severity-tag">{card.severity}</span>
	</div>
	<div class="name">
		{card.name}
	</div>
	<div class="footer">
		Due: {card.due_date}
	</div>
</button>

<style>
	.card {
		background-color: white;
		box-sizing: border-box;
		border: 1px solid #ffffff;
		border-radius: 12px;
		min-height: 46px;
		max-height: fit-content;
		padding: 1em;
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 1em;
		cursor: grab;
	}
	.name {
		width: 100%;
		text-align: start;
		font-size: 1rem;
		font-weight: 550;
	}
	.header,
	.footer {
		display: flex;
		justify-content: space-between;
	}
	.tag-tag,
	.severity-tag {
		border-radius: 14px;
		box-sizing: border-box;
		padding: 2px 8px;
		color: white;
		font-weight: 550;
	}
	.severity-tag {
		background-color: green;
	}
	.tag-tag {
		background-color: #7c6bff;
	}
	.footer {
		font-weight: 500;
		color: red;
	}
	.card-detail-dlg {
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		padding: 2em;
		outline: none;
		width: max-content;
		border: 2px solid #d2d2d2;
		border-radius: 14px;
		align-items: center;
		background-color: white;
		width: max-content;
	}
	.card-detail-dlg:not([open]) {
		display: none;
	}
	.card-detail-div {
		display: flex;
		flex-direction: column;
		box-sizing: border-box;
		gap: 1em;
		> .major-detail {
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			align-items: start;

			> .topleft {
				display: flex;
				flex-direction: column;
				gap: 0.8em;
				> .detail-title {
					display: flex;
					flex-direction: row;
					gap: 8px;
					> h1 {
						margin: 0;
						font-weight: 550;
						font-size: 1.4rem;
					}
				}
			}
		}
	}
	.tags {
		display: flex;
		flex-direction: column;
		padding-left: 2.2em;
		gap: 0.4em;
		> div {
			display: flex;
			gap: 8px;
		}
	}
	.date {
		display: flex;
		flex-direction: column;

		padding-left: 2.2em;

		> label {
			display: flex;
			gap: 8px;
			> button {
				background-color: #ba1a1add;
				color: white;
				font-weight: 550;
				padding: 4px 12px;
				border: 1px solid #ba1a1a;
				border-radius: 4px;
				cursor: pointer;
			}
		}
	}
	.date > span,
	.tags > span {
		font-weight: 600;
		opacity: 60%;
		font-size: 16px;
		margin-bottom: 4px;
	}
	.desc-detail {
		display: flex;
		flex-direction: column;
		> p {
			padding-left: 2em;
			height: max-content;
			font-size: 14px;
			font-weight: 500;
			color: #101010dd;
		}
	}
	.desc-title {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		> div {
			display: flex;
			gap: 8px;
			> span {
				font-weight: 600;
				font-size: 1.2rem;
			}
		}
		> button {
			font-size: 14px;
			font-weight: 550;
			padding: 2px 12px;
			color: #101010dd;
			background-color: #e1e1e1;
			border: 1px solid #c1c1c1;
			border-radius: 4px;
			cursor: pointer;
		}
	}
	.checklist-detail {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.checklist-title {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		> div {
			display: flex;
			gap: 8px;
			> span {
				font-weight: 600;
				font-size: 1.2rem;
			}
		}
		> button {
			font-size: 14px;
			font-weight: 550;
			padding: 2px 12px;
			color: #101010dd;
			background-color: #e1e1e1;
			border: 1px solid #c1c1c1;
			border-radius: 4px;
			cursor: pointer;
		}
	}
	.checklist-list {
		padding-left: 2.1em;
		display: flex;
		flex-direction: column;
		gap: 0.6em;
	}
	.checklist-item {
		position: relative;
		display: flex;
		flex-direction: row;
		width: 80%;
		align-items: center;
		justify-content: space-between;
		> div {
			display: flex;
			gap: 6px;
			> span {
				font-weight: 550;
				color: #202020;
			}
			> input {
				cursor: pointer;
			}
		}
	}
	.checked-by {
		> summary {
			list-style: none;
			cursor: pointer;
			background-color: #0051b8;
			padding: 0.6em;
			box-sizing: border-box;
			align-items: center;
			display: flex;
			justify-content: center;
			color: white;
			border-radius: 50%;
			width: 28px;
			height: 28px;
		}
		> strong {
			position: absolute;
			right: -3.8em;
			background-color: #e1e1e1;
			padding: 0.2em 0.6em;
			z-index: 100;
			border-radius: 8px;
		}
	}
	.new-item-btn {
		text-align: start;
		box-sizing: border-box;
		padding-left: 1.6em;
		height: 28px;
		font-weight: 550;
		opacity: 80%;
		cursor: pointer;
		background-color: transparent;
		border: none;
	}
	.new-checklist-btn {
		height: 32px;
		border-radius: 6px;
		border: 1px solid #0051b8;
		background-color: #0051b8dd;
		color: white;
		font-weight: 550;
		cursor: pointer;
		box-shadow: 4px 4px 12px #20202040;
	}
	.new-checklist-btn:active {
		box-shadow: none;
	}
	svg {
		width: 24px;
	}
	code {
		background-color: #ba1a1a55;
		box-sizing: border-box;
		padding: 2px 8px;
		font-weight: 600;
		font-size: 14px;
		border-radius: 4px;
		border: 2px solid #ba1a1a;
	}
</style>
