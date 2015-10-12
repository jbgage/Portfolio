@angular.module('AngularD3Voronoi' , [])
.directive('voronoi' ,  () ->
		restrict: 'EA',
		scope:{
			data: '=',
			width: '=',
			height: '='
		},
		link: (scope , element) ->
			
				margin = {top:20,right:20,bottom:20,left:40}
				width = scope.width - margin.left - margin.right
				height = scope.height - margin.top - margin.bottom
				voronoi = d3.geom.voronoi()
					.clipExtent([[0, 0], [width, height]]);
				svg = d3.select(element[0])
					.append('svg')
					.attr('width' , width )
					.attr('height' , height)
				path = svg.append("g").selectAll("path")
				
				scope.render = (data) ->
					polygon = (d) ->
						"M" + d.join("L") + "Z"
					
					redraw = ->
						path = path.data(voronoi(scope.data) , polygon)
						path.exit().remove()
						path.enter().append("path")
							.attr("d" , polygon)
						path.order()
						return
					svg.selectAll('circle')
						.data(scope.data.slice(1))
						.enter()
						.append('circle')
						.attr('transform' , (d) ->
							"translate(" + d + ")"
						)
						.attr('r' , 1.5)
					redraw()
					return
					
					
				scope.$watch('data' , () ->
					scope.render(scope.data)
					return
				, true)	
				return
			
			
)