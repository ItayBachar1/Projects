public class GraphEdge {
    GraphNode u;
    GraphNode v;
    GraphEdge prevIn;
    GraphEdge nextIn;
    GraphEdge prevOut;
    GraphEdge nextOut;

    public GraphEdge(GraphNode f, GraphNode t ){
        this.u = f;
        this.v = t;
    }
}
