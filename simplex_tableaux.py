def simplex_tableaux(c,A_ub=[],b_ub=[],var_names=[],slack_names=[],tol=1e-4,dec=2,colormap='Greys'):
    # (C) Ganesh Sriram, gsriram@umd.edu
    # Licensed under GNU Public License 3.0
    
    # This script implements the simplex method for solving LPs in the form of matrix operations
    # It was written specifically for CHBE444: ChE Design I, University of Maryland
  
    # This version supports only inequality constraints (equality constraints are not permitted)
    # This version does not update the auxiliary after each pivot

    # Changelog
    # v. 1.3
    #     A and b are now called A_ub and b_ub for consistency with linprog
    #     var_names and/or slack_names may be left blank if user wants the algorithm to create them
    #     tol is used to avoid lots of iterations with little/no incremental benefit
    #     Tlist is returned as a list of pandas dataframes with headers
     
    # c: cost vector for objective function
    # A_ub: inequality matrix (coefficients of x_i in inequalities)
    # b_ub: inequality vector (constants in inequalities)
    # var_names and slack_names: headers
    # A and c should have the same number of columns (equal to the number of variables)
    # A and b should have the same number of rows (equal to the number of constraints)
    
    
    import numpy as np
    import pandas as pd


    A = A_ub
    b = b_ub
    
    # Examine vectors and matrix dimensions for consistency
    # Create headers (variable and slack names) if not provided
    
    Arows = np.size(A,axis=0)
    Acols = np.size(A,axis=1)
    brows = np.size(b)
    ccols = np.size(c)

    assert Acols == ccols, 'Check input dimensions. A and c have different numbers of columns.'
    assert Arows == brows, 'Check input dimensions. A and b have different numbers of rows.'

    if var_names == []:  # create var_names if empty
        var_names = [f'x{j}' for j in range(1,1+Acols)]  # Acols and ccols would have been checked for consistency by now                                                      
    
    var_num = np.size(var_names)
    var_max = max(int(s.lstrip('x')) for s in var_names)

    if slack_names == []:
        slack_names = [f'x{i}' for i in range(var_max+1,var_max+1+Arows)]  # Arows and brows would have been checked for consistency by now
    
    slack_min = min(int(s.lstrip('x')) for s in slack_names)
    
    if slack_names == [] or slack_min <= var_max:  # create slack_names if empty or index is <= var_max
        slack_names = [f'x{i}' for i in range(var_max+1,var_max+1+Arows)]  # Arows and brows would have been checked for consistency by now
            
    slack_num = np.size(slack_names)
        
    assert Acols == var_num, 'Check input dimensions. The number of original variables is different from the number of columns of A.'    
    assert Arows == slack_num, 'Check input dimensions. The number of slack variables is different from the number of rows of A.'
       
    
    # Process LP and create initial tableau
    
    n = np.size(c)  # count number of original variables
    m = np.size(b)  # count number of slack variables
    
    def sleq(i,m):  # function to get the ith row of a mxm identity matrix
        I = np.identity(m)
        return I[i]

    T = np.concatenate(([1],c,np.zeros(m),[0]),0)  # construct initial tableau T
   
    for i in range(0,m):
        t = np.concatenate(([0],A[i],sleq(i,m),[b[i]]),0)  # current row
        T = np.vstack((T,t))  # append current row below T
    
    Trows = np.size(T,axis=0)
    Tcols = np.size(T,axis=1)
    
    aux_needed = False  # compose auxiliary objective if needed
    
    c_aux = np.zeros(Tcols)  # initialize cost vector for auxiliary objective
    for i in range(1,1+m):
        if T[i,Tcols-1] < 0:
            aux_needed = True
            c_aux += T[i]  # update cost vector for auxiliary objective
    
    if aux_needed == True:
        T = np.insert(T,1,c_aux,axis=0)
        t = np.concatenate(([0],[1],np.zeros(m)),0)
        T = np.insert(T,1,t,axis=1)
    
    if aux_needed == False:
        row_names = ["z"]
    else:
        row_names = ["z","z'"]
       
    for k in range(0,np.size(slack_names)):
        row_names.append(slack_names[k])
    
    if aux_needed == False:
        col_names = ["z"]
    else:
        col_names = ["z","z'"]
    
    for j in range(0,np.size(var_names)):
        col_names.append(var_names[j])
    for i in range(0,np.size(slack_names)):
        col_names.append(slack_names[i])
    col_names.append('b')

    Tlist = [pd.DataFrame(T,columns=col_names,index=row_names)]  # store tableau in a list
    
    
    # Use pandas to display T as a tableau
    
    def conditionally_format_initial(styler):
        styler.background_gradient(axis=None,vmin=np.min(T),vmax=np.max(T),cmap=colormap)
        return styler
   
    df = pd.DataFrame(T,columns=col_names,index=row_names)
    df_style = df.style.format(precision=dec).pipe(conditionally_format_initial).set_properties(
        **{'text-align':'center'})
    df_style.set_table_styles([{'selector':'th.col_heading','props':'text-align: center;'},],overwrite=False)
    display(df_style)  
    
    Trows = np.size(T,axis=0)
    Tcols = np.size(T,axis=1)

    if aux_needed == True:
        start = 2
        index = 1
    else:
        start = 1
        index = 0

        
    # Iterate
    
    stop_condition = False
    
    while stop_condition == False:
        if aux_needed == True and T[1,Tcols-1] >= 0:
            aux_needed = False
            index = 0
        
        pcol = 0  # initialize pivot column
        cval = tol 
            
        for j in range(start,start+m+n):
            if T[index,j] < tol and T[index,j] < cval:
                cval = T[index,j]
                pcol = j  # identify pivot column
        if cval == 0:
            stop_condition = True
       
        if stop_condition == False:
            prow = 0  # initialize pivot row
            rval = np.inf
            for i in range(start,start+m):
                if T[i,pcol] > 0 and T[i,Tcols-1]/T[i,pcol] < rval:
                    rval = T[i,Tcols-1]/T[i,pcol]
                    prow = i  # identify pivot row

                       
            # Perform pivot
            
            R = np.identity(Trows)  # initialize pivoting matrix R to identity matrix
            
            factors = -T[:,pcol]/T[prow,pcol]  # factors to ensure that pivot column elements above and below pivot 
                                               # row are zero after pivot
            factors[prow] = 1;  # pivot row is unaltered during pivot
            R[:,prow] = factors
            
            T = np.dot(R,T)  # pivot operation
            
            row_names[prow] = col_names[pcol]  # update row headers

            Tlist.append(pd.DataFrame(T,columns=col_names,index=row_names))  # append tableau to the list
            
            
            def conditionally_format_current(styler):
                styler.background_gradient(axis=None,vmin=np.min(T),vmax=np.max(T),cmap=colormap)
                return styler
            
            df = pd.DataFrame(T,columns=col_names,index=row_names)
            df_style = df.style.format(precision=dec).pipe(conditionally_format_current).set_properties(
                **{'text-align':'center'})
            df_style.set_table_styles([{'selector':'th.col_heading','props':'text-align: center;'},],overwrite=False)
            display(df_style)
               
    return Tlist  # return the list of tableaux as dataframes