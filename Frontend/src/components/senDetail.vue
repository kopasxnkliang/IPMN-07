<template>
	<div :class="'bodyBox'">
		<el-collapse v-model="activeSentence" accordion :class="'collapseBox'" >
				<el-collapse-item v-for="(sen, index) in Sentences" 
				v-bind:name="sen.ID" :class="'sentenceBox'">
				<template #title v-if="activeSentence==sen.ID">
					<div :class="'titleBox'">
						<h2 style="display: contents;">Sentence {{index+1}} Detail</h2>
						<div :class="'detailButBox'">	
							<el-tooltip effect="dark" content="Delete this sentence">
								<el-button type="info" :icon="Delete" 
								@click.stop="deleteSenClick"/>
							</el-tooltip>
							<el-tooltip effect="dark" content="Copy this sentence" >
								<el-button type="info" :icon="CopyDocument" 
								@click.stop="clipSmallClick" style="margin-left: 5px;"/>
							</el-tooltip>
							<el-tooltip effect="dark" content="Generate this sentence" >
								<el-button type="info" :icon="Refresh" 
								:loading="sen.senLoading" @click.stop="generateSenClick" 
								style="margin-left: 5px;"/>
							</el-tooltip>
						</div>
					</div>
					
				</template>
				<template #title v-else  >
					<div :class="'omittedBox'">
						<div :class="'omittedRelat'">
							<el-tag v-for="r in sen.Relation" 
							:class="'relationTag'" type="info" :key="r"> 
								{{r}} 
							</el-tag>
						</div>
						<div :class="'omittedText'">
							<el-skeleton :rows="0" v-if="sen.senLoading || sen.Text==''" animated ></el-skeleton>
							<p v-else :class="'omittedTextShow'">{{sen.Text}}</p>
						</div>
					</div>
					
				</template>
				<div :class="'SentenceBody'">
					<div :class="'relation'">
						<el-tag v-for="r in sen.Relation" 
						:class="'relationTag'" type="info" closable 
						:key="r" @close="closeTag(r)" @click="tagClick(r)">
							{{r}}
						</el-tag>
						<div :class="'inputTriple'" v-if="formVisible" style="font-size: 12px;">
							
							<el-input v-model="tripleSet1" size="small" :style="{width:calTextLen(tripleSet1,50)}"
							placeholder="Word1" clearable :class="'input'" autosize></el-input>
							
							<el-autocomplete v-model="tripleSet2"
							:style="{width:calTextLen(tripleSet2,65)}"
							:fetch-suggestions="querySearch" style="margin-left: 2px;;"
							clearable placeholder="Relation" :class="'input'" size="small"
							></el-autocomplete>
							<el-input v-model="tripleSet3" style="margin-left: 2px;"
							:style="{width:calTextLen(tripleSet3,50)}"
							placeholder="Word2" clearable :class="'input'" size="small"></el-input>
							<el-button type="info" circle style="margin-left: 12px;"
							@click="cancelButtonClick" :icon="Close" size="small"></el-button>
							<el-button type="info" circle style="margin-left: 2px;"
							@click="SaveButtonClick" :icon="Check" size="small"></el-button>
						</div>
            <div :class="'inputTriple'" v-if="changeFormVisible" style="font-size: 12px;">

              <el-input v-model="tripleSet1" size="small" :style="{width:calTextLen(tripleSet1,50)}"
                        placeholder="Word1" clearable :class="'input'" autosize></el-input>

              <el-autocomplete v-model="tripleSet2"
                               :style="{width:calTextLen(tripleSet2,65)}"
                               :fetch-suggestions="querySearch" style="margin-left: 2px;;"
                               clearable placeholder="Relation" :class="'input'" size="small"
              ></el-autocomplete>
              <el-input v-model="tripleSet3" style="margin-left: 2px;"
                        :style="{width:calTextLen(tripleSet3,50)}"
                        placeholder="Word2" clearable :class="'input'" size="small"></el-input>
              <el-button type="info" circle style="margin-left: 12px;"
                         @click="tagCancelButtonClick" :icon="Close" size="small"></el-button>
              <el-button type="info" circle style="margin-left: 2px;"
                         @click="tagEditButtonClick" :icon="Check" size="small"></el-button>
            </div>
						<el-button plain :icon="Plus" 
						:class="'relationTag'" @click="formVisible=true" v-else></el-button>
					</div>

					<div :class="'SenText'">
						<el-skeleton :rows="2" v-if="sen.senLoading || sen.Text==''" animated ></el-skeleton>
						<el-input v-else v-model="sen.Text" 
						type="textarea"  :autosize="{ minRows: 5 }"></el-input>
					</div>
				</div>
				</el-collapse-item>
		</el-collapse>
		<div :class="'buttonSlip'">
			<el-button plain :icon="Plus" :class="'addButton'" 
			@click="addsenButtonClick">Add a sentence</el-button>
			<el-button plain :icon="CopyDocument" :class="'copyButton'" 
			@click="clipBigClick">Copy all sentences</el-button>
		</div>
	</div>
</template>

<script setup>
import useClipboard from "vue-clipboard3";
import {Delete, Plus, CopyDocument,Check,Close,Refresh} from '@element-plus/icons-vue'
import { ref,onMounted } from 'vue';
import {ElMessage } from 'element-plus' 
import axios from "axios";

// generate a random int (max=100000000) as base id
const baseID = Math.floor(Math.random()*100000000)

// activate id of el-collapse
let activeSentence = ref(-1)

// input box of triple sets
let tripleSet1 = ref('')
let tripleSet2 = ref('')
let tripleSet3 = ref('')
let tmpTripleSet = ''

// count for sentences, used to generate sentence ID
let count = 1

// search domain of el-autocomplete
const recommends = ["main subject",'follow','have part', 'participant','location', 'part of', 'subsidiary', 
					'instance of']
// search results that is needed to be shown in el-autocomplete
const recommendRelation = ref([])

// visilibablity of input triples
let formVisible = ref(false)

// visilibablity of change triples
let changeFormVisible = ref(false)

// server url (based on vite.config.js)
const serverIP = "/api/example"

// sentences that need to be shown on screen
let Sentences = ref([])

// generate structure used in el-autocomplete
function constructRecom(){
	let ret = []
	for(var i=0;i<recommends.length;i++){
		ret.push({'value':recommends[i]})
	}
	return ret
}

// load autocomplete list when mount the web
onMounted(()=>{
	recommendRelation.value = constructRecom()
	// Sentences.value = constructSenTest()
})

// search a sentence with certain ID
function findSen(idx){
	for (var i=0; i<Sentences.value.length; i++){
		if (Sentences.value[i].ID == idx){
			return i
		}
	}
	return -1
}

// delete triple set
function closeTag(tag){
	var curid = findSen(activeSentence.value)
	if (curid ==-1 ){
		return
	}
	Sentences.value[curid].Relation.splice(Sentences.value[curid].Relation.indexOf(tag),1)
}

// search words that is similar in el-autocomplete, return a filter
const createFilter = (queryString) => {
	return (words) =>{
		return (
			words.value.toLowerCase().indexOf(queryString.toLowerCase())===0
		)
	}
}

// search words that is similar in el-autocomplete
const querySearch = (queryString, cb) => {
	const results = queryString 
	? recommendRelation.value.filter(createFilter(queryString))
	:recommendRelation.value
	cb(results)
}

// click action when triple set is clicked, open edit form
function tagClick(tag){
  tmpTripleSet = tag.valueOf()
  const tripleSet = tag.valueOf().split(" | ")
  tripleSet1.value = tripleSet[0]
  tripleSet2.value = tripleSet[1]
  tripleSet3.value = tripleSet[2]
  changeFormVisible.value = true
}

// end edit and save
function tagEditButtonClick(){
  if (tripleSet1.value === "" || tripleSet2.value === "" || tripleSet3.value === ""){
    tagCancelButtonClick()
    return
  }
  var tripleSet = tripleSet1.value+' | '+tripleSet2.value+' | '+tripleSet3.value
  var curid = findSen(activeSentence.value)

  Sentences.value[curid].Relation[Sentences.value[curid].Relation.indexOf(tmpTripleSet)] = tripleSet
  changeFormVisible.value = false
  tripleSet1.value = ""
  tripleSet2.value = ""
  tripleSet3.value = ""
  tmpTripleSet.value = ""

}

// close edit form and remove all possible changes
function tagCancelButtonClick(){
  tripleSet1.value = ""
  tripleSet2.value = ""
  tripleSet3.value = ""
  changeFormVisible.value = false
}

// save a input triple set
function SaveButtonClick(){
	if (tripleSet1.value=="" || tripleSet2.value == "" || tripleSet3.value == ""){
		cancelButtonClick()
		return
	}
	var tripleSet = tripleSet1.value.trim()+' | '+tripleSet2.value.trim()+' | '+tripleSet3.value.trim()
	var curid = findSen(activeSentence.value)
	
	Sentences.value[curid].Relation.push(tripleSet)
	tripleSet1.value = ""
	tripleSet2.value = ""
	tripleSet3.value = ""
	formVisible.value = false
}

// close add form
function cancelButtonClick(){
	tripleSet1.value = ""
	tripleSet2.value = ""
	tripleSet3.value = ""
	formVisible.value = false
}

// add a sentence
function addsenButtonClick(){
	count++
	var newid = baseID + count
	Sentences.value.push({
		ID: newid,
		Relation:[],
		Text:'',
		senLoading:false
	})
	activeSentence.value = newid
}

// copy the input text to clipboard
async function clipText(text){
	const { toClipboard } = useClipboard()
	try {
		await toClipboard(text)
		ElMessage("Copy to clipboard success, empty sentences is missed.")
	} catch(e){
		console.error(e)
	}
}

// copy all not empty sentences to clipboard
function clipBigClick(){
	var text = new String
	for (var i=0;i<Sentences.value.length;i++){
		text += Sentences.value[i].Text
	}
	clipText(text)
}

// copy a sentence to clipboard
function clipSmallClick(){
	var curid = findSen(activeSentence.value)
	clipText(Sentences.value[curid].Text)
}

// delete a sentence
function deleteSenClick(){
	var curid = findSen(activeSentence.value)
	if (curid==-1){
		return
	}
	Sentences.value.splice(curid,1)
	activeSentence.value = -1
}

// send a request to backend to generate a sentence
function generateSenClick(idx){
	// 1. get cur id
	var curid = findSen(activeSentence.value)
	
	// 2. generate post data
	const postData = {
		ID: Sentences.value[curid].ID,
		Relation: Sentences.value[curid].Relation
	}
	
	// 3. set loading state
	Sentences.value[curid].senLoading = true
	
	// 4. send request
	axios.post(serverIP,postData)
		 .then(function(response){
			 // console.log(response.data)
			 // if success
			 // console.log(response.data.Text)
			 let id = findSen(response.data.ID)
			 if (id == -1){
				 return
			 }
			 Sentences.value[id].Text = response.data.Text
			 Sentences.value[id].senLoading = false
			 
		 })
		 .catch(function(error){
			 console.error(error)
		 })
}

// calculate the real length of text that is shown on screen
function calTextLen(src, defal){
	// console.error(src)
	if (src.length == 0){
		return defal+'px'
	}
	var width = 0;
	var html = document.createElement('span');
	html.innerText = src;
	html.className = 'getTextWidth';
	html.style = "font-size: 12px;"
	document.querySelector('body').appendChild(html);
	width = document.querySelector('.getTextWidth').offsetWidth;
	document.querySelector('.getTextWidth').remove();
	// console.error(width)
	return width+36+'px';

}


</script>

<style>
	
	.bodyBox{
		margin: auto;
		max-width: 80%;
		display: grid;
		gap: 8px;
	}
	
	.collapseBox{
		display: grid;
		gap: 8px;
	}
	
	.relationTag{
		display: flex;
		text-align: center;
		/* Set */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 6px 5px;
		gap: 5px;
		
		width: fit-content;
		height: 29px;
		
		border: 1px solid #000000;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;
		
	}
	
	.TripleSet{
		
		/* word1 | word2 | word3 */
		
		width: auto;
		height: 15px;
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 12px;
		line-height: 15px;
		/* identical to box height */
		display: flex;
		align-items: center;
		
		color: #000000;
		
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;

	}
	
	.SetDeleteButton{
		/* image 2 */
		
		width: auto;
		height: auto;
				
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;

	}

	.relation{
		/* ↓ relation tripes [container] */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: flex-start;
		align-content: flex-start;
		padding: 4px;
		gap: 10px;
		
		width: 45%	;
		height: fit-content;
		min-height: 115px;
		
		border: 1px solid #D6D5D5;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 1;
	}

	.SentenceBody{
		/* sentence body */
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		padding: 10px;
		padding-bottom: 0px;
		gap: 10px;
		
		min-height: 130px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		align-self: stretch;
		flex-grow: 0;
	}

	.SenText{
		/* sentence(loaded) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 0px 4px;
		gap: 10px;
		
		width: 45%;
		height: fit-content;
		min-height: 115px;
		
/* 		border: 1px solid #D6D5C5;
		border-radius: 4px; */
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		align-self: stretch;
		flex-grow: 1;

	}

	.sentenceBox{
		/* sentence 2(el-collapse) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		padding: 10px 11px;
		
		width: 1209px;
		/* height: 206px; */
		
		border: 1px solid #525252;
		border-radius: 15px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;
		
	}

	.buttonSlip{
		/* Button slip */
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 0px;
		
		width: 100%;
		height: 65px;
		
		
		/* Inside auto layout */
		flex: none;
		order: 2;
		align-self: stretch;
		flex-grow: 0;
	}

	.addButton{
		/* Add button */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 3px 0px;
		
/* 		width: 1012px;
		height: 65px; */
		width: 80%;
		height: 100%;
		
		border: 1px solid #000000;
		border-radius: 10px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 1;		
		
			
		/* Add a sentence */
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 15px;
		line-height: 18px;
		display: flex;
		align-items: center;
		text-align: center;
		
		color: #000000;

	}

	.copyButton{
		/* Copy button */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 3px 0px;
		
		width: 15%;
		height: 100%;
		
		border: 1px solid #000000;
		border-radius: 10px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;
		
		/* Copy all sentences */
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 15px;
		line-height: 18px;
		display: flex;
		align-items: center;
		text-align: center;
		
		color: #000000;

	}

	.omittedRelat{
		/* relation tripes */
		
		box-sizing: border-box;
		overflow: hidden;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		align-items: center;
		padding: 0px 4px;
		gap: 15px;
		margin-right: 20px;
		
		width: 45%;
		height: 100%;
		
		border: 1px solid #D6D5D5;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		align-self: stretch;
		flex-grow: 1;
	}

	.omittedBox{
		/* sentence 1 (el-collapse) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		/* padding: 10px 11px; */
		gap: 10px;
		
		width: calc(100% - 21px);
		height: 100%;
		
/* 		border: 1px solid #525252;
		border-radius: 15px; */
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;

	}

	.omittedText{
		/* sentence(loading) */
		
		width: 50%;		
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}
	
	.omittedTextShow{
		width: 100%;
		height: auto;
		max-height: 100%;
		margin: 0 0 0 0;
		font-size: 12px;
		line-height: normal;
	}

	.inputBox{
		display: flex;
		gap: 15px;
		justify-content: center;
	}
	
	.input{
		width: auto;
	}

	.formButton{
		margin-top: 15px;
		text-align: right;
		padding-right: 6%;
	}

	.titleBox{
		display: flex;
		flex-grow: 1;
		justify-content: space-between;
		height: 100%;
		padding-left: 10px;
	}
	
	[role="tab"]{
		width: 100%;
	}
	
	[role="button"]{
		border-bottom: 0px;
	}
	
	.el-collapse-head-6598{
		width: 100%;
	}
	
	.detailButBox{
		display: flex;
		align-content: center;
		flex-direction: row;
		align-items: center;
		margin-right: 10px;
	}
	
	.el-collapse-item__content{
		padding-bottom: 15px;
	}
	
	.el-collapse-item__wrap{
		width: 100%;
	}

	.inputTriple{
		font-size: 12px;
		display: flex;
		
		flex-direction: row;
		flex-wrap: wrap;
		align-content: center;
		justify-content: flex-start;
		align-items: stretch;
		
		max-width: 100%;
		height: auto;
		min-height: 29px;
		width: auto;
		flex-direction: row;
		justify-content: space-evenly;
		align-items: center;
		padding: 0px 4px;
		border: 1px solid #000000;
		border-radius: 4px;
		background-color: rgb(244, 244, 245);
	}
</style>