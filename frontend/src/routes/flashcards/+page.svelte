<script lang="ts">
    import '$lib/tailwind.css'
    import { page } from "$app/stores";
    import { shuffle } from '$lib/utils';
    const termsRaw = $page.url.searchParams.get("terms")?.split?.(",");
    let terms: [string, string][] = [];

    if(termsRaw) {
        for(let i = 0; i < termsRaw.length; i += 2) {
            terms.push([termsRaw[i], termsRaw[i + 1]]);
        }
    }

    // pick up to 6 random terms
    if(terms.length > 6) {
        shuffle(terms);
        terms = terms.slice(0, 6);
    }

    interface Card {
        flipped: boolean;
        correct: boolean;
        text: string;
        match?: Card;
    }

    let cards: Card[] = [];

    for(let pair of terms) {
        let card1: Card = {
            flipped: false, correct: false,
            text: pair[0],
        }
        let card2: Card = {
            flipped: false, correct: false,
            text: pair[1],
            match: card1
        }

        card1.match = card2;
        cards.push(card1);
        cards.push(card2);
    }

    let flippedCards: Card[] = [];
    let waiting = false;
    let successDialog: HTMLDialogElement;

    async function clickCard(card: Card) {
        if(card.flipped || waiting) return;

        card.flipped = true;
        
        flippedCards.push(card);
        if(flippedCards.length === 2) {

            // check if they match
            if(flippedCards[0].match !== flippedCards[1]) {
                cards = [...cards];
                waiting = true;
                await new Promise(resolve => setTimeout(resolve, 1500));
                flippedCards[0].flipped = false;
                flippedCards[1].flipped = false;
                waiting = false;
            } else {
                flippedCards[0].correct = true;
                flippedCards[1].correct = true;

                // check if all cards are correct
                if(cards.every(card => card.correct)) {
                    successDialog.showModal();
                }
            }
            
            flippedCards = [];
        }
        
        cards = [...cards];
    }
    
    // crappy shuffle
    shuffle(cards);
</script>

<div class="grid grid-cols-6 p-8 gap-y-3">
    {#each cards as card}
        <div class="w-full h-full flex justify-center items-center">
            <button class="card w-48 relative"
            class:flipped={card.flipped} class:correct={card.correct}
            on:click={() => clickCard(card)}>
                <img src="/cardBack.png" alt="The Back of a Playing Card" class="cardBack" />
                <img src="/cardFront.png" alt="The Back of a Playing Card" class="cardFront" />
                <div class="term">{card.text}</div>
            </button>
        </div>
    {/each}
</div>

<dialog class="rounded p-5 border-4 border-blue-300 bg-blue-100" bind:this={successDialog}>
    <h1 class="w-full text-center text-3xl">You win!</h1>
    <div class="w-full flex items-center justify-center">
        <button class="hover:border-purple-300 rounded bg-blue-100 border-blue-300 p-3 m-10"
        on:click={() => location.reload()}>Play Again</button>
    </div>
</dialog>

<style>
    .cardBack, .term, .cardFront {
        backface-visibility: hidden;
        transition: transform 0.5s;
    }

    .term, .cardFront {
        transform: rotateY(180deg);
    }
    
    .term {
        width: 100%;
        text-align: center;
        padding: 15px;
    }

    .card.correct {
        filter: drop-shadow(0 0 0.5rem blue);
    }

    .card {
        width: 200px;
        height: 300px;
    }
    
    .card > * {
        position: absolute;
        top: 0px;
        left: 0px;
    }

    .card.flipped .cardBack {
        transform: rotateY(180deg);
    }

    .card.flipped .term, .card.flipped .cardFront {
        transform: rotateY(0deg);
    }
</style>