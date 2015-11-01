@angular.module('AngularD3Voronoi' , [])
.directive('voronoi' ,  () ->
	if d3?
		restrict: 'EA',
		scope:{
			vertices: '@'
		},
		link: (scope , element , attr) ->
			margin = {top:20,right:20,bottom:20,left:40}
			width = attr.width - margin.left - margin.right
			height = attr.height - margin.top - margin.bottom
			scope.render = (data) ->
					results = eval(data)
					voronoi = d3.geom.voronoi().clipExtent([[0 , 0] , [width , height]])
					svg = d3.select(element[0])
							.append('svg')
							.attr('width' , width)
							.attr('height' , height)
					path = svg.append('g')
							  .selectAll('path')
					colors = d3.scale.category20c()
					if results.length > 0 
						svg.selectAll('path')
						   .data(voronoi(results))
						   .enter()
						   .append('path')
						   .style('fill' , (d , i) ->
						   		return colors(i)
						   )
						   .attr('d' , (d) ->
						   		return 'M' + d.join('L') + 'Z'
						   )
			scope.$watch('vertices' , (data) ->
					scope.render(data)
			, true)	
	else
		throw new Error('This directive requires d3.js. Please include this file in your script references.')
				
)