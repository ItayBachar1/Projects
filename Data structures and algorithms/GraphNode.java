public class GraphNode {
    private int key;
    public DoublyLinkedListEdge inEdgeList ;
    public DoublyLinkedListEdge outEdgeList;
    public DoublyLinkedListNode nodeList;
    GraphNode leftChild = null;
    GraphNode rightSibling = null;
    GraphNode lastRight = null;
    GraphNode parent = null;
    GraphNode next = null;
    GraphNode prev = null;
    GraphNode nextQ = null;
    GraphNode prevQ = null;
    String color ;
    int d;
    int f;

    public GraphNode(int k) {
        this.key = k;
        inEdgeList = new DoublyLinkedListEdge();
        outEdgeList = new DoublyLinkedListEdge();
        nodeList = new DoublyLinkedListNode();
    }

    void setKey(int nodeKey){
        this.key = nodeKey;
    }

    public int getOutDegree(){
        GraphEdge pointer = outEdgeList.getHead();
        if(pointer==null)
            return 0;
        int count=1;
        while(pointer.nextOut!=null) {
            count++;
            pointer = pointer.nextOut;
        }
        return count;

    }

    public int getInDegree(){
        GraphEdge pointer = inEdgeList.getHead();
        if(pointer==null)
            return 0;
        int count=1;
        while(pointer.nextIn!=null) {
            count++;
            pointer = pointer.nextIn;
        }
        return count;
    }

    public int getKey(){
        return key;
    }
}
