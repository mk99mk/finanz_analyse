<script lang="ts">
	import { sub_pages } from '$lib/Navigation.svelte';
	import { onMount } from 'svelte';

	$sub_pages = [{ href: '#', name: 'TradeRepublic' }];

	let chart_source: string | undefined = undefined;
	onMount(() => {
		chart_source = '/api/depot/tr';
	});
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">See your stocks here</h2>
		<div class="flex justify-center space-x-2">
			{#if chart_source}
				<iframe width="1300px" height="700px" src={chart_source} title="description"></iframe>
			{/if}
		</div>
	</div>
</div>
