// Graph visualization setup
const width = document.getElementById('graph-container').clientWidth;
const height = document.getElementById('graph-container').clientHeight;

const svg = d3.select('#graph-container')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

const g = svg.append('g');

// Add zoom behavior
const zoom = d3.zoom()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {
        g.attr('transform', event.transform);
    });

svg.call(zoom);

// Force simulation setup
const simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(30));

// Control force parameters
d3.select('#charge-force').on('input', function() {
    simulation.force('charge').strength(+this.value);
    simulation.alpha(1).restart();
});

d3.select('#link-distance').on('input', function() {
    simulation.force('link').distance(+this.value);
    simulation.alpha(1).restart();
});

const tooltip = d3.select('.tooltip');

// Fetch and render graph data
fetch('/api/graph')
    .then(response => response.json())
    .then(data => {
        // Update statistics
        const stats = {
            nodes: data.nodes.length,
            relationships: data.relationships.length,
            labels: new Set(data.nodes.flatMap(n => n.labels)).size,
            relationshipTypes: new Set(data.relationships.map(r => r.type)).size
        };

        const statsHtml = Object.entries(stats).map(([key, value]) => `
            <div class="stat-item">
                <span class="stat-label">${key.charAt(0).toUpperCase() + key.slice(1)}</span>
                <span class="stat-value">${value}</span>
            </div>
        `).join('');

        document.getElementById('graph-stats').innerHTML = statsHtml;

        // Create links with arrows
        const links = g.selectAll('.link')
            .data(data.relationships)
            .enter()
            .append('line')
            .attr('class', 'link');

        // Create nodes
        const nodes = g.selectAll('.node')
            .data(data.nodes)
            .enter()
            .append('circle')
            .attr('class', 'node')
            .attr('r', 15)
            .attr('fill', d => {
                const label = d.labels[0];
                switch(label) {
                    case 'Disease': return '#ff7f7f';
                    case 'Protein': return '#7fbf7f';
                    case 'Autism': return '#7f7fff';
                    default: return '#999';
                }
            })
            .on('mouseover', (event, d) => {
                tooltip.style('display', 'block')
                    .html(`
                        <strong>${d.labels.join(', ')}</strong><br>
                        ${Object.entries(d.properties)
                            .map(([key, value]) => `${key}: ${value}`)
                            .join('<br>')}
                    `);
            })
            .on('mousemove', (event) => {
                tooltip.style('left', (event.pageX + 10) + 'px')
                       .style('top', (event.pageY - 10) + 'px');
            })
            .on('mouseout', () => {
                tooltip.style('display', 'none');
            })
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));

        // Add node labels
        const labels = g.selectAll('.node-label')
            .data(data.nodes)
            .enter()
            .append('text')
            .attr('class', 'node-label')
            .text(d => d.properties.name || d.labels[0])
            .attr('dx', 20)
            .attr('dy', 4);

        // Update simulation
        simulation
            .nodes(data.nodes)
            .on('tick', ticked);

        simulation.force('link')
            .links(data.relationships);

        // Simulation tick function
        function ticked() {
            links
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            nodes
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);

            labels
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        }
    });

// Drag functions
function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// Handle window resize
window.addEventListener('resize', () => {
    const width = document.getElementById('graph-container').clientWidth;
    const height = document.getElementById('graph-container').clientHeight;
    
    svg.attr('width', width).attr('height', height);
    simulation.force('center', d3.forceCenter(width / 2, height / 2));
    simulation.alpha(1).restart();
});