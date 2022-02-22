<template>
	<view class="buttons" hover-class="buttons-hover" :style="parameter" hover-stay-time="80" @click="pressButton">
		<!-- 使用view而不是button的原因：使用button会有一个去不掉的难看的框 -->
		<slot />
	</view>
</template>

<script>
	export default {
		name: "weiyang-button",
		data() {
			return {}
		},
		props: {
			type: { // 内置样式
				type: String,
				default: 'normal'
			},
			bgcolor: {
				type: String,
				default: '#0087A9'
			},
			hovercolor: {
				type: String,
				default: '#00657F'
			},
			duration: {
				type: Number,
				default: 80
			},
			hasShadow: {
				type: Boolean,
				default: false
			}
		},
		computed: {
			parameter() {
				let parameter = {
					'--bg-color': this.bgcolor,
					'--hover-color': this.hovercolor,
					'--duration': this.duration + 'ms',
					'--has-shadow': this.hasShadow
				}
				switch (this.type) {
					case 'green':
						parameter['--bg-color'] = '#00BF00'
						parameter['--hover-color'] = '#008C00'
						break;
					case 'red':
						parameter['--bg-color'] = '#EB3341'
						parameter['--hover-color'] = '#B82834'
						break
					case 'blue':
						parameter['--bg-color'] = '#009FFF'
						parameter['--hover-color'] = '#007ECC'
						break
				}
				return parameter
			}
		},
		emits: ['click'],
		methods: {
			pressButton(e) {
				this.$emit('click', e)
			}
		}
	}
</script>

<style scoped lang="scss">
	@keyframes ripple {
		0% {
			background-image: radial-gradient(circle at center, var(--hover-color) 20%, var(--bg-color));
		}

		10% {
			background-image: radial-gradient(circle at center, var(--hover-color) 28%, var(--bg-color));
		}

		20% {
			background-image: radial-gradient(circle at center, var(--hover-color) 36%, var(--bg-color));
		}

		30% {
			background-image: radial-gradient(circle at center, var(--hover-color) 44%, var(--bg-color));
		}

		40% {
			background-image: radial-gradient(circle at center, var(--hover-color) 52%, var(--bg-color));
		}

		50% {
			background-image: radial-gradient(circle at center, var(--hover-color) 60%, var(--bg-color));
		}

		70% {
			background-image: radial-gradient(circle at center, var(--hover-color) 76%, var(--bg-color));
		}

		80% {
			background-image: radial-gradient(circle at center, var(--hover-color) 84%, var(--bg-color));
		}

		90% {
			background-image: radial-gradient(circle at center, var(--hover-color) 92%, var(--bg-color));
		}

		100% {
			background-image: radial-gradient(circle at center, var(--hover-color) 100%, var(--bg-color));
		}
	}

	$duration: var(--duration);

	.buttons {
		margin: 0 10rpx;
		padding: 10rpx 20rpx;
		border-radius: 30rpx;

		color: #FFFFFF;
		text-align: center;
		font: 600 36rpx sans-serif;
		background: var(--bg-color);

		@if var(--has-shadow)==true {
			box-shadow: 0 3rpx 8rpx rgba(0, 0, 0, 0.3);
			/* black with 30% opacity */
		}

		transform: scale(1);
		transition: transform calc($duration/2);
		transition-timing-function: ease-in-out;
	}

	.buttons-hover {
		transform: scale(0.98);
		animation: ripple $duration linear forwards;
	}
</style>
