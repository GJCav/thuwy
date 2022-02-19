<template>
	<view class="col-container">
		<weiyang-section subtitle="我是副标题">
			<weiyang-forms  @submit="test"></weiyang-forms>
		</weiyang-section>
		<!-- <button @click="test()">从脚底超级</button> -->
		
		<view v-for="item in sample" :key="item">
			<weiyang-card :pattern="item">{{'卡片角标'}}</weiyang-card>
		</view>
	</view>
</template>

<script>
	const app=getApp()
	export default {
		data() {
			return {
				value:'',
				sample:[11,12,13,21,22,31,32,33,34],	// 所用卡片样式一览
				valiFormData: {
					name: '',
					age: '',
					introduction: '',
				},
				// 校验规则
				rules: {
					name: {
						rules: [{
							required: true,
							errorMessage: '姓名不能为空'
						}]
					},
					age: {
						rules: [{
							required: true,
							errorMessage: '年龄不能为空'
						}, {
							format: 'number',
							errorMessage: '年龄只能输入数字'
						}]
					}
				},
			}
		},
		methods: {
			test(e){
				console.log(e)
			},
		}
	}
</script>

<style>
 uni-easyinput{
	 background-color: #000000;
 }
</style>
