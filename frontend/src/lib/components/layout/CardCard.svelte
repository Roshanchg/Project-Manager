<script lang="ts">
	import type { CardDetails, CardInfo } from "$lib/types";


    type Props={
        card: CardInfo;
        getDetails?:(card:CardInfo)=>CardDetails | null;
    };

    let {card,getDetails}:Props=$props();

    function pass(){
        getDetails?.(card);
    }

</script>

<button onclick={pass} class="card">
    <div class="header">
        <span class="tag-tag" >{card.tag}</span>
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
    .card{
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
    .name{
        width: 100%;
        text-align: start;
        font-size: 1rem;
        font-weight: 550;
    }
    .header,.footer{
        display: flex;
        justify-content: space-between;
    }
    .tag-tag,.severity-tag{
        border-radius: 14px;
        box-sizing: border-box;
        padding: 2px 8px;
        color: white;
        font-weight: 550;
    }
    .severity-tag{
        background-color: green;
    }
    .tag-tag{
        background-color: #7C6BFF;
    }
    .footer{
        font-weight: 500;
        color: red;
    }
</style>