public class DoublyLinkedListEdge {
    GraphEdge head;
    GraphEdge tail;

    public void insertHeadIn(GraphEdge value) {
        value.nextIn = this.head;
        if (this.head == null) {
            this.tail = value;
        }
        else {
            this.head.prevIn = value;
        }
        this.head = value;
        value.prevIn = null;
    }

    public void insertHeadOut(GraphEdge value) {
        value.nextOut = this.head;
        if (this.head == null) {
            this.tail = value;
        }
        else {
            this.head.prevOut = value;
        }
        this.head = value;
        value.prevOut = null;
    }

    public void insertTail(GraphEdge value) {
        value.prevOut = this.tail;
        if(this.tail==null){
            this.head=value;
        }
        else{
            this.tail.nextOut = value;
        }
        this.tail=value;
        value.nextOut = null;

    }

    public void deleteEdgeOut(GraphEdge edge) {
        if(edge==null)
            return;
        if(edge.nextOut!=null){
            if(edge.prevOut!=null){
                edge.prevOut.nextOut = edge.nextOut;
                edge.nextOut.prevOut = edge.prevOut;
            }
            else{
                edge.nextOut.prevOut = null;
                this.head = edge.nextOut;
            }
        }
        else{
            if(edge.prevOut!=null){
                edge.prevOut.nextOut = null;
                this.tail = edge.prevOut;
            }
            else{
                this.head=null;
                this.tail=null;
            }
        }
        edge.nextOut =null;
        edge.prevOut =null;
    }

    public void deleteEdgeIn(GraphEdge node) {
        if(node==null)
            return;
        if(node.nextIn!=null){
            if(node.prevIn!=null){
                node.prevIn.nextIn = node.nextIn;
                node.nextIn.prevIn = node.prevIn;
            }
            else{
                node.nextIn.prevIn = null;
                this.head = node.nextIn;
            }
        }
        else{
            if(node.prevIn!=null){
                node.prevIn.nextIn = null;
                this.tail = node.prevIn;
            }
            else{
                this.head=null;
                this.tail=null;
            }
        }
        node.nextIn =null;
        node.prevIn =null;
    }

    public GraphEdge getHead() {
        return this.head;
    }

    public GraphEdge getTail() {
        return this.tail;
    }

}
