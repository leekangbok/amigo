import lazyloading from './lazyLoading'

export default [{
  text: '라이브스트리밍',
  path: '/liveStream',
  icon: 'view_stream',
  pri: 301,
  component: lazyloading('liveStream', true)
}]
