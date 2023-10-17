import holoviews as hv
from holoviews import dim, opts

hv.extension('matplotlib')
hv.output(fig='png')

nodes = ["PhD", "Career Outside Science",  "Early Career Researcher", "Research Staff",
         "Permanent Research Staff",  "Professor",  "Non-Academic Research"]
nodes = hv.Dataset(enumerate(nodes), 'index', 'label')
edges = [
    (0, 1, 53), (0, 2, 127), (2, 6, 17), (2, 3, 30), (3, 1, 22.5), (3, 4, 3.5), (3, 6, 4.), (4, 5, 0.45)   
]

value_dim = hv.Dimension('Percentage', unit='%')
fig = hv.Sankey((edges, nodes), ['From', 'To'], vdims=value_dim).opts(
    opts.Sankey(cmap='Set1', labels='label', label_position='right', fig_size=300,
                edge_color=dim('To').str(), node_color=dim('index').str()))

hv.save(fig, "test.png")