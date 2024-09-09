<script lang="ts">
	import { sub_pages } from '$lib/Navigation.svelte';
	import { onMount } from 'svelte';
	import { depotsApiDepotsGet } from '../../client';
	import { page } from '$app/stores';
	import type { Page } from '@sveltejs/kit';

	let chart_source: string | undefined = undefined;

	async function load_page(page: Page<Record<string, string>, string | null>) {
		const search_param = page.url.searchParams;
		if (search_param.size === 0) return;
		const name = search_param.get('depot');
		if (name == undefined) return;

		console.log('depot ', name);
		chart_source = `/api/depot/${name}`;
	}

	async function load() {
		// console.log('search ', $page.url.searchParams);
		page.subscribe(load_page);

		chart_source = '/api/all_depots';
		const depots = await depotsApiDepotsGet();
		const depots_objs = [];
		if (depots.data == undefined) return;
		for (const depot of depots.data) {
			depots_objs.push({ href: `/stocks?depot=${depot}`, name: depot });
		}
		console.log('depots obj ', depots_objs);
		$sub_pages = depots_objs;
	}

	onMount(load);
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
