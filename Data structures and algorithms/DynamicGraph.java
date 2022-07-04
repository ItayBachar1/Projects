public class DynamicGraph {
    DoublyLinkedListNode listNode;
    DoublyLinkedListNode dfsQ;

    public DynamicGraph() {
         listNode = new DoublyLinkedListNode();
         dfsQ = new DoublyLinkedListNode();
    }

    public GraphNode insertNode(int nodeKey) {
        GraphNode node = new GraphNode(nodeKey);
        listNode.insertHead(node);
        return node;
    }

    public void deleteNode(GraphNode node) {
        if (node.inEdgeList.getHead() != null || node.outEdgeList.getHead() != null)
            return;
        this.listNode.deleteNode(node);

    }

    public GraphEdge insertEdge(GraphNode from, GraphNode to) {
        GraphEdge newEdge = new GraphEdge(from, to);
        from.outEdgeList.insertHeadOut(newEdge);
        to.inEdgeList.insertHeadIn(newEdge);
        return newEdge;
    }

    public void deleteEdge(GraphEdge edge) {
        edge.u.outEdgeList.deleteEdgeOut(edge);
        edge.v.inEdgeList.deleteEdgeIn(edge);
    }


    static int time;

    public RootedTree scc() {
        GraphNode p = listNode.getHead();
        while(p!=null){
            p.prevQ=null;
            p.nextQ=null;
            p=p.next;
        }
        this.dfsQ = new DoublyLinkedListNode();
        GraphNode s1 = this.dfs(false);

        GraphNode s = this.dfs(true);

        RootedTree T = new RootedTree();
        T.root = s;
        p = listNode.getHead();
        while(p!=null){
            p.prevQ=null;
            p.nextQ=null;
            p=p.next;
        }
        return T;
    }

    public GraphNode dfs(boolean second) {
        if (!second) {
            GraphNode p = listNode.getHead();
            GraphNode u;
            while (p != null) {
                p.prevQ = null;
                p.nextQ = null;
                p = p.next;
            }
            u = listNode.getHead();
            while (u != null) {
                u.color = "white";
                u.parent = null;
                u.leftChild = null;
                u.rightSibling = null;
                u.prevQ = null;
                u.nextQ = null;
                u = u.next;
            }
            time = 0;
            u = listNode.getHead();
            while (u != null) {
                if (u.color.equals("white")) {
                    dfs_visit(u, second);
                }
                u = u.next;
            }
            return listNode.getHead();
        }
        else{
            GraphNode u;
            u = dfsQ.getHead();

            GraphNode s0 = new GraphNode(0);
            while (u != null) {
                u.color = "white";
                u.parent = null;
                u.leftChild = null;
                u.rightSibling = null;
                u = u.nextQ;
            }
            time = 0;
            u = dfsQ.getHead();

            while (u != null) {
                if (u.color.equals("white")) {
                    addChild(u, s0);
                    dfs_visit(u, second);

                }
                u=u.nextQ;
            }

            return s0;
        }
    }

    private void dfs_visit(GraphNode u, boolean second) {
        if(!second) {
            time++;
            u.d = time;
            u.color = "gray";
            GraphEdge e;
            GraphNode node;
            e = u.outEdgeList.getHead();
            while (e != null) {
                node = e.v;
                if (node.color.equals("white")) {
                    node.parent = u;
                    this.dfs_visit(node, second);
                }
                e = e.nextOut;
            }
            u.color = "black";
            time++;
            u.f = time;
            dfsQ.insertHeadQ(u);
        }
        else{
            time++;
            u.d = time;
            u.color = "gray";
            GraphEdge e;
            GraphNode node;
            e = u.inEdgeList.getHead();
            while (e != null) {
                node = e.u;
                if (node.color.equals("white")) {
                    node.parent = u;
                    addChild(node, u);
                    this.dfs_visit(node, second);
                }
                e = e.nextIn;
            }
            u.color = "black";
            time++;
            u.f = time;
        }

    }

    public void addChild(GraphNode child, GraphNode parent){
        if(parent.leftChild==null)
            parent.leftChild= child;
        else{
            addRight(child, parent.leftChild);
        }

    }

    public void addRight(GraphNode child, GraphNode parent){
        if(child==null)
            return;
        while(parent.rightSibling!=null)
            parent = parent.rightSibling;
        parent.rightSibling = child;
    }


    public RootedTree bfs(GraphNode source) {
        DoublyLinkedListNode Q = this.bfs_initialization(source);
        GraphNode node =null;
        GraphNode prevChild = source;
        while (Q.getHead() != null) {
            GraphNode u = Q.getHead();
            Q.deleteHeadQ(Q.getHead());                         //u=deq
            GraphEdge edgePointer = u.outEdgeList.getHead(); // Adj list
            if(edgePointer!=null) {
                node = edgePointer.v; // node from the edge
                while(!node.color.equals("white")){
                    edgePointer = edgePointer.nextOut;
                    if(edgePointer == null)
                        break;
                    node = edgePointer.v;
                }
                if (node.color.equals("white")) {
                    u.leftChild = node;// the first child
                    prevChild = node;
                }
            }
            while (edgePointer != null) {    //Adj list
                if (node.color.equals("white")) {
                    prevChild = node;
                    node.color = "gray";
                    node.d = u.d + 1;
                    node.parent = u;
                    Q.insertTailQ(node);
                }
                edgePointer = edgePointer.nextOut;
                if(edgePointer!=null) {
                    if (edgePointer.v.color.equals("white"))
                        prevChild.rightSibling = edgePointer.v;
                    node = edgePointer.v;
                }

            }
            u.color = "black";

        }
        GraphNode p = listNode.getHead();
        while(p!=null){
            p.prevQ=null;
            p.nextQ=null;
            p=p.next;
        }
        RootedTree newTree = new RootedTree();
        newTree.root = source;
        return newTree;
    }

    private DoublyLinkedListNode bfs_initialization(GraphNode s) {
        GraphNode v = this.listNode.getHead();
        while (v != null) {
            v.color = "white";
            v.d = Integer.MAX_VALUE;
            v.parent = null;
            v.nextQ = null;
            v.prevQ = null;
            v.leftChild = null;
            v.rightSibling = null;
            v = v.next;
        }
        s.color = "gray";
        s.d = 0;
        s.parent = null;
        s.leftChild = null;
        s.rightSibling = null;
        s.nextQ = null;
        s.prevQ = null;
        DoublyLinkedListNode Q = new DoublyLinkedListNode();
        Q.insertTailQ(s);
        return Q;
    }

}